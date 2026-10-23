using System.Reflection;

namespace HomeScout.CostEngine.Tests;

[TestFixture]
internal sealed class AssemblySmokeTests
{
    [Test]
    public void AssemblyMarker_assemblyIsLoaded_hasCostEngineName()
    {
        Assembly assembly = typeof(AssemblyMarker).Assembly;

        Assert.That(assembly.GetName().Name, Is.EqualTo("HomeScout.CostEngine"));
    }
}
