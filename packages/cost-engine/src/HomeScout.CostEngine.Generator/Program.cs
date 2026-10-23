using System.Text.Json;
using HomeScout.CostEngine.Generator;

// Usage: dotnet run --project packages/cost-engine/src/HomeScout.CostEngine.Generator [path to packages/fixtures]
// Writes packages/fixtures/generated/costs.json from packages/fixtures/data.
// Exits 0 on success, 1 when the cost engine reports a problem (its error code is printed, nothing is written),
// and 2 when a data file is missing or cannot be understood.
try
{
    string fixtures = args.Length > 0
        ? Path.GetFullPath(args[0])
        : Path.Combine(FindRepositoryRoot(Directory.GetCurrentDirectory()), "packages", "fixtures");

    int exit = CostsGenerator.Run(fixtures, Console.Error);
    if (exit == 0)
    {
        Console.WriteLine($"Generated {Path.Combine(fixtures, "generated", CostsGenerator.FileName)}");
    }

    return exit;
}
catch (Exception exception) when (exception is IOException or InvalidDataException or JsonException or UnauthorizedAccessException)
{
    Console.Error.WriteLine($"Generator could not run: {exception.Message}");
    return 2;
}

static string FindRepositoryRoot(string startDirectory)
{
    DirectoryInfo? directory = new(startDirectory);
    while (directory is not null)
    {
        if (File.Exists(Path.Combine(directory.FullName, "HomeScout.slnx")))
        {
            return directory.FullName;
        }

        directory = directory.Parent;
    }

    throw new DirectoryNotFoundException($"HomeScout.slnx not found above {startDirectory}.");
}
