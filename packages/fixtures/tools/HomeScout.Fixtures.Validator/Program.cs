using HomeScout.Fixtures.Validator;

// Usage: dotnet run --project packages/fixtures/tools/HomeScout.Fixtures.Validator [path to packages/fixtures]
// Exits 0 when every file is valid, 1 when something is wrong (each problem is printed), 2 on a setup error.
string fixtures;
try
{
    fixtures = args.Length > 0
        ? Path.GetFullPath(args[0])
        : Path.Combine(FixtureValidator.FindRepositoryRoot(Directory.GetCurrentDirectory()), "packages", "fixtures");
}
catch (DirectoryNotFoundException exception)
{
    Console.Error.WriteLine(exception.Message);
    return 2;
}

IReadOnlyList<FixtureProblem> problems = FixtureValidator.ValidateFixtures(fixtures);
if (problems.Count == 0)
{
    Console.WriteLine("Fixtures: every data file and test case matches its schema.");
    return 0;
}

foreach (FixtureProblem problem in problems)
{
    Console.Error.WriteLine(problem.ToString());
}

Console.Error.WriteLine($"Fixtures: {problems.Count} problem(s) found.");
return 1;
