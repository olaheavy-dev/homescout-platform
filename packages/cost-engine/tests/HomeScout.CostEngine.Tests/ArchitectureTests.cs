using System.Reflection;
using System.Reflection.Emit;
using NetArchTest.Rules;

namespace HomeScout.CostEngine.Tests;

/// <summary>
/// Keeps the cost engine a pure library (decisions 0019, 0021, 0027): no files, network, HTTP, cloud, AI, clock or
/// randomness, no outside packages, and no binary floating point in what it exposes.
/// Each rule is also run against something that does break it, so a rule that can never fail is noticed.
/// </summary>
[TestFixture]
internal sealed class ArchitectureTests
{
    private static readonly Assembly _engine = typeof(Pence).Assembly;

    private static readonly string[] _forbiddenNamespaces =
    [
        "System.IO",
        "System.Net",
        "System.Data",
        "System.Diagnostics.Process",
        "System.Security.Cryptography",
        "Microsoft.Extensions.Http",
        "Microsoft.Extensions.AI",
        "Microsoft.AspNetCore",
        "Azure",
        "OpenAI",
        "Anthropic",
        "Npgsql",
    ];

    // Types whose use means the clock or randomness. DateTime itself is allowed: only reading the current time is not.
    private static readonly string[] _forbiddenClockAndRandomTypes =
    [
        "System.TimeProvider",
        "System.Random",
        "System.Threading.Timer",
        "System.Diagnostics.Stopwatch",
    ];

    // Under `make test` the coverage tool adds its own tracker types to the engine assembly; they are not engine code.
    private const string _coverageNamespace = "Coverlet";

    private static readonly string[] _clockMembers = ["get_Now", "get_UtcNow", "get_Today"];

    [Test]
    public void CostEngine_assembly_hasNoDependencyOnIoNetworkCloudOrAi()
    {
        TestResult result = Types.InAssembly(_engine).That().DoNotResideInNamespaceStartingWith(_coverageNamespace).ShouldNot().HaveDependencyOnAny(_forbiddenNamespaces).GetResult();

        Assert.That(result.FailingTypeNames, Is.Null.Or.Empty);
    }

    [Test]
    public void CostEngine_assembly_hasNoDependencyOnClockOrRandom()
    {
        TestResult result = Types.InAssembly(_engine).That().DoNotResideInNamespaceStartingWith(_coverageNamespace).ShouldNot().HaveDependencyOnAny(_forbiddenClockAndRandomTypes).GetResult();

        Assert.That(result.FailingTypeNames, Is.Null.Or.Empty);
    }

    [Test]
    public void CostEngine_assembly_neverReadsTheCurrentTime() =>
        Assert.That(CurrentTimeReaders(_engine), Is.Empty);

    [Test]
    public void CostEngine_assembly_referencesOnlyTheFrameworkAndSystemLibraries()
    {
        IEnumerable<string> outsiders = _engine.GetReferencedAssemblies()
            .Select(a => a.Name ?? string.Empty)
            .Where(n => !n.StartsWith("System.", StringComparison.Ordinal) && n is not ("System" or "netstandard" or "mscorlib"));

        Assert.That(outsiders, Is.Empty);
    }

    [Test]
    public void CostEngine_publicSignatures_useNoDoubleOrFloat() =>
        Assert.That(PublicSignaturesUsingBinaryFloatingPoint(_engine), Is.Empty);

    // Self-checks: each rule above must be able to fail, so run it on a type that does break it.

    [Test]
    public void DependencyRule_appliedToCodeThatUsesFiles_failsAsExpected()
    {
        TestResult result = Types.InAssembly(typeof(ArchitectureTests).Assembly)
            .That().HaveName(nameof(RuleBreaker))
            .ShouldNot().HaveDependencyOnAny(_forbiddenNamespaces).GetResult();

        Assert.That(result.IsSuccessful, Is.False);
    }

    [Test]
    public void ClockRule_appliedToCodeThatReadsTheTime_failsAsExpected()
    {
        Assert.That(CurrentTimeReaders(typeof(ArchitectureTests).Assembly), Has.Some.Contain(nameof(RuleBreaker)));
    }

    [Test]
    public void FloatingPointRule_appliedToCodeThatExposesDouble_failsAsExpected()
    {
        Assert.That(PublicSignaturesUsingBinaryFloatingPoint(typeof(ArchitectureTests).Assembly), Has.Some.Contain(nameof(RuleBreaker)));
    }

    private static IEnumerable<Type> EngineTypes(Assembly assembly) =>
        assembly.GetTypes().Where(t => t.Namespace?.StartsWith(_coverageNamespace, StringComparison.Ordinal) != true);

    /// <summary>Lists "Type.Method" for every method that calls DateTime.Now, UtcNow, Today or the DateTimeOffset equivalents.</summary>
    private static List<string> CurrentTimeReaders(Assembly assembly)
    {
        var readers = new List<string>();
        Dictionary<short, OpCode> opCodes = typeof(OpCodes)
            .GetFields(BindingFlags.Public | BindingFlags.Static)
            .Select(f => (OpCode)f.GetValue(null)!)
            .ToDictionary(o => o.Value);

        const BindingFlags all = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Static | BindingFlags.DeclaredOnly;
        foreach (Type type in EngineTypes(assembly))
        {
            foreach (MethodBase method in type.GetMethods(all).Cast<MethodBase>().Concat(type.GetConstructors(all)))
            {
                if (CallsClock(method, opCodes))
                {
                    readers.Add($"{type.FullName}.{method.Name}");
                }
            }
        }

        return readers;
    }

    private static bool CallsClock(MethodBase method, Dictionary<short, OpCode> opCodes)
    {
        byte[]? il = method.GetMethodBody()?.GetILAsByteArray();
        if (il is null)
        {
            return false;
        }

        int position = 0;
        while (position < il.Length)
        {
            OpCode opCode = il[position] == 0xFE
                ? opCodes[(short)(0xFE00 | il[position + 1])]
                : opCodes[il[position]];
            position += opCode.Size;

            if (opCode.OperandType == OperandType.InlineMethod)
            {
                int token = BitConverter.ToInt32(il, position);
                MethodBase? called = method.Module.ResolveMethod(token, method.DeclaringType?.GetGenericArguments(), method.IsGenericMethod ? method.GetGenericArguments() : null);
                if (called is { DeclaringType.FullName: "System.DateTime" or "System.DateTimeOffset" } && _clockMembers.Contains(called.Name))
                {
                    return true;
                }
            }

            position += OperandSize(opCode, il, position);
        }

        return false;
    }

    private static int OperandSize(OpCode opCode, byte[] il, int position) => opCode.OperandType switch
    {
        OperandType.InlineNone => 0,
        OperandType.ShortInlineBrTarget or OperandType.ShortInlineI or OperandType.ShortInlineVar => 1,
        OperandType.InlineVar => 2,
        OperandType.InlineI8 or OperandType.InlineR => 8,
        OperandType.InlineSwitch => 4 + (4 * BitConverter.ToInt32(il, position)),
        _ => 4,
    };

    /// <summary>Lists "Type.Member" for every public or protected member (of any type, which is stricter than only exported types) whose type, parameter or return type is double or float.</summary>
    private static List<string> PublicSignaturesUsingBinaryFloatingPoint(Assembly assembly)
    {
        var found = new List<string>();
        const BindingFlags visible = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Static | BindingFlags.DeclaredOnly;

        foreach (Type type in EngineTypes(assembly))
        {
            foreach (MemberInfo member in type.GetMembers(visible))
            {
                if (IsExposed(member) && MemberTypes(member).Any(IsOrContainsBinaryFloatingPoint))
                {
                    found.Add($"{type.FullName}.{member.Name}");
                }
            }
        }

        return found;
    }

    private static bool IsExposed(MemberInfo member) => member switch
    {
        MethodBase m => m.IsPublic || m.IsFamily || m.IsFamilyOrAssembly,
        FieldInfo f => f.IsPublic || f.IsFamily || f.IsFamilyOrAssembly,
        PropertyInfo p => (p.GetMethod?.IsPublic ?? false) || (p.GetMethod?.IsFamily ?? false) || (p.SetMethod?.IsPublic ?? false) || (p.SetMethod?.IsFamily ?? false),
        EventInfo e => e.AddMethod?.IsPublic ?? false,
        _ => false,
    };

    private static IEnumerable<Type> MemberTypes(MemberInfo member) => member switch
    {
        MethodInfo m => m.GetParameters().Select(p => p.ParameterType).Append(m.ReturnType),
        ConstructorInfo c => c.GetParameters().Select(p => p.ParameterType),
        FieldInfo f => [f.FieldType],
        PropertyInfo p => p.GetIndexParameters().Select(i => i.ParameterType).Append(p.PropertyType),
        EventInfo e => e.EventHandlerType is null ? [] : [e.EventHandlerType],
        _ => [],
    };

    private static bool IsOrContainsBinaryFloatingPoint(Type type)
    {
        if (type == typeof(double) || type == typeof(float))
        {
            return true;
        }

        if (type.HasElementType)
        {
            return IsOrContainsBinaryFloatingPoint(type.GetElementType()!);
        }

        return type.IsGenericType && type.GetGenericArguments().Any(IsOrContainsBinaryFloatingPoint);
    }

    /// <summary>Deliberately breaks every rule above, so the self-checks have something to catch. Never used.</summary>
    internal static class RuleBreaker
    {
        public static double ExposedDouble { get; } = 0.5;

        public static DateTime Now() => DateTime.Now;

        public static bool FileExists(string path) => File.Exists(path);

        public static float Combine(IReadOnlyList<float> values) => values.Count;
    }
}
