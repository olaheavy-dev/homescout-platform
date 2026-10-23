using System.Reflection;
using System.Reflection.Emit;
using System.Runtime.InteropServices;
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

    private static readonly string[] _forbiddenJsonNamespaces = ["System.Text.Json", "Newtonsoft"];

    // Types whose use means the clock or randomness. DateTime itself is allowed: only reading the current time is not.
    private static readonly string[] _forbiddenClockAndRandomTypes =
    [
        "System.TimeProvider",
        "System.Random",
        "System.Threading.Timer",
        "System.Diagnostics.Stopwatch",
        "System.Environment",
    ];

    // Under `make test` the coverage tool adds its own tracker types to the engine assembly; they are not engine code.
    // Only this exact namespace is excluded; every other type must live under HomeScout.CostEngine.
    private const string _coverageNamespace = "Coverlet.Core.Instrumentation.Tracker";

    private const string _engineNamespace = "HomeScout.CostEngine";

    // Calls that read the clock or make something new and unpredictable: DateTime/DateTimeOffset Now, UtcNow, Today and Guid.NewGuid.
    private static readonly string[] _forbiddenMembers =
    [
        "System.DateTime.get_Now",
        "System.DateTime.get_UtcNow",
        "System.DateTime.get_Today",
        "System.DateTimeOffset.get_Now",
        "System.DateTimeOffset.get_UtcNow",
        "System.Guid.NewGuid",
    ];

    [Test]
    public void CostEngine_assembly_hasNoDependencyOnIoNetworkCloudOrAi()
    {
        TestResult result = Types.InAssembly(_engine).That().DoNotResideInNamespaceStartingWith(_coverageNamespace).ShouldNot().HaveDependencyOnAny(_forbiddenNamespaces).GetResult();

        Assert.That(result.FailingTypeNames, Is.Null.Or.Empty);
    }

    [Test]
    public void CostEngine_assembly_hasNoDependencyOnSystemTextJson()
    {
        // The engine works on plain values; reading and writing JSON is the generator's job (plan 4b, section 2).
        TestResult result = Types.InAssembly(_engine).That().DoNotResideInNamespaceStartingWith(_coverageNamespace).ShouldNot().HaveDependencyOnAny(_forbiddenJsonNamespaces).GetResult();

        Assert.That(result.FailingTypeNames, Is.Null.Or.Empty);
    }

    [Test]
    public void JsonRule_appliedToCodeThatUsesJson_failsAsExpected()
    {
        TestResult result = Types.InAssembly(typeof(ArchitectureTests).Assembly)
            .That().HaveName(nameof(RuleBreaker))
            .ShouldNot().HaveDependencyOnAny(_forbiddenJsonNamespaces).GetResult();

        Assert.That(result.IsSuccessful, Is.False);
    }

    [Test]
    public void CostEngine_assembly_hasNoDependencyOnClockOrRandom()
    {
        TestResult result = Types.InAssembly(_engine).That().DoNotResideInNamespaceStartingWith(_coverageNamespace).ShouldNot().HaveDependencyOnAny(_forbiddenClockAndRandomTypes).GetResult();

        Assert.That(result.FailingTypeNames, Is.Null.Or.Empty);
    }

    [Test]
    public void CostEngine_assembly_neverReadsTheClockOrMakesGuids() =>
        Assert.That(ForbiddenMemberCallers(_engine), Is.Empty);

    [Test]
    public void CostEngine_assembly_referencesOnlyTheFrameworkAndSystemLibraries()
    {
        Assert.That(ReferencesOutsideTheFramework(_engine), Is.Empty);
    }

    [Test]
    public void CostEngine_everyTypeOutsideTheCoverageTracker_livesUnderTheEngineNamespace()
    {
        // The C# compiler adds helper types for collection expressions and constant arrays (for example
        // <PrivateImplementationDetails>). Their names start with '<', which no C# type of ours can, so they are not engine code.
        IEnumerable<string> strays = EngineTypes(_engine)
            .Where(t => !t.Name.StartsWith('<') && !(t.DeclaringType?.Name.StartsWith('<') ?? false))
            .Where(t => t.FullName?.StartsWith(_engineNamespace, StringComparison.Ordinal) != true)
            .Select(t => t.FullName ?? t.Name);

        Assert.That(strays, Is.Empty);
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
        Assert.That(ForbiddenMemberCallers(typeof(ArchitectureTests).Assembly), Has.Some.Contain(nameof(RuleBreaker)));
    }

    [Test]
    public void ClockAndRandomTypeRule_appliedToCodeThatUsesRandom_failsAsExpected()
    {
        TestResult result = Types.InAssembly(typeof(ArchitectureTests).Assembly)
            .That().HaveName(nameof(RuleBreaker))
            .ShouldNot().HaveDependencyOnAny(_forbiddenClockAndRandomTypes).GetResult();

        Assert.That(result.IsSuccessful, Is.False);
    }

    [Test]
    public void ForbiddenMemberRule_appliedToCodeThatCallsGuidNewGuid_failsAsExpected() =>
        Assert.That(ForbiddenMemberCallers(typeof(ArchitectureTests).Assembly), Has.Some.Contain(nameof(RuleBreaker.NewId)));

    [Test]
    public void FrameworkOnlyRule_appliedToTheTestAssembly_failsAsExpected() =>
        Assert.That(ReferencesOutsideTheFramework(typeof(ArchitectureTests).Assembly), Has.Some.Contain("NUnit"));

    [Test]
    public void FloatingPointRule_appliedToCodeThatExposesDouble_failsAsExpected()
    {
        Assert.That(PublicSignaturesUsingBinaryFloatingPoint(typeof(ArchitectureTests).Assembly), Has.Some.Contain(nameof(RuleBreaker)));
    }

    private static IEnumerable<Type> EngineTypes(Assembly assembly) =>
        assembly.GetTypes().Where(t => t.FullName?.StartsWith(_coverageNamespace, StringComparison.Ordinal) != true);

    /// <summary>
    /// Lists referenced assemblies that are not in the shared .NET framework folder. Checking the folder, not the name,
    /// means a NuGet package called System.Something does not pass.
    /// </summary>
    private static List<string> ReferencesOutsideTheFramework(Assembly assembly)
    {
        string frameworkDirectory = RuntimeEnvironment.GetRuntimeDirectory();

        return assembly.GetReferencedAssemblies()
            .Select(a => a.Name ?? string.Empty)
            .Where(n => !File.Exists(Path.Combine(frameworkDirectory, n + ".dll")))
            .ToList();
    }

    /// <summary>Lists "Type.Method" for every method that calls one of the forbidden members above.</summary>
    private static List<string> ForbiddenMemberCallers(Assembly assembly)
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
                if (CallsForbiddenMember(method, opCodes))
                {
                    readers.Add($"{type.FullName}.{method.Name}");
                }
            }
        }

        return readers;
    }

    private static bool CallsForbiddenMember(MethodBase method, Dictionary<short, OpCode> opCodes)
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
                if (called is not null && _forbiddenMembers.Contains($"{called.DeclaringType?.FullName}.{called.Name}"))
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

        public static Guid NewId() => Guid.NewGuid();

#pragma warning disable CA5394 // Deliberately insecure randomness: this type exists to break the rules.
        public static int Dice() => Random.Shared.Next();
#pragma warning restore CA5394

        public static bool FileExists(string path) => File.Exists(path);

        public static string AsJson(int value) => System.Text.Json.JsonSerializer.Serialize(value);

        public static float Combine(IReadOnlyList<float> values) => values.Count;
    }
}
