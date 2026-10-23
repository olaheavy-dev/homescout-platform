namespace HomeScout.CostEngine.Tests;

/// <summary>Finds files in the repository, so tests read the real worked examples and never copies of them.</summary>
internal static class RepositoryFiles
{
    private static readonly string _root = FindRoot(AppContext.BaseDirectory);

    public static string TestCases(string fileName) =>
        Path.Combine(_root, "packages", "fixtures", "test-cases", fileName);

    private static string FindRoot(string start)
    {
        DirectoryInfo? directory = new(start);
        while (directory is not null)
        {
            if (File.Exists(Path.Combine(directory.FullName, "HomeScout.slnx")))
            {
                return directory.FullName;
            }

            directory = directory.Parent;
        }

        throw new InvalidOperationException($"HomeScout.slnx not found above {start}.");
    }
}
