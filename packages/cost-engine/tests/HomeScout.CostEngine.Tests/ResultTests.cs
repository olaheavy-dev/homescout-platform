namespace HomeScout.CostEngine.Tests;

[TestFixture]
internal sealed class ResultTests
{
    private static readonly string[] _decidedCategories = ["Validation", "NotFound", "Conflict", "Unavailable"];

    private static readonly Error _sample = new("input.missing", "A required figure is missing.", ErrorCategory.Validation);

    [Test]
    public void Success_noValue_isSuccessWithNoError()
    {
        Result result = Result.Success();

        Assert.That(result.IsSuccess, Is.True);
        Assert.That(result.IsFailure, Is.False);
        Assert.That(() => result.Error, Throws.TypeOf<InvalidOperationException>());
    }

    [Test]
    public void Failure_withError_isFailureCarryingThatError()
    {
        Result result = Result.Failure(_sample);

        Assert.That(result.IsSuccess, Is.False);
        Assert.That(result.IsFailure, Is.True);
        Assert.That(result.Error, Is.EqualTo(_sample));
    }

    [Test]
    public void Failure_nullError_throwsArgumentNullException() =>
        Assert.That(() => Result.Failure(null!), Throws.TypeOf<ArgumentNullException>());

    [Test]
    public void SuccessOfT_withValue_exposesValue()
    {
        Result<Pence> result = Result.Success(new Pence(42));

        Assert.That(result.IsSuccess, Is.True);
        Assert.That(result.Value, Is.EqualTo(new Pence(42)));
        Assert.That(() => result.Error, Throws.TypeOf<InvalidOperationException>());
    }

    [Test]
    public void FailureOfT_withError_hidesValueAndExposesError()
    {
        Result<Pence> result = Result.Failure<Pence>(_sample);

        Assert.That(result.IsFailure, Is.True);
        Assert.That(result.Error, Is.EqualTo(_sample));
        Assert.That(() => result.Value, Throws.TypeOf<InvalidOperationException>());
    }

    [Test]
    public void FailureOfT_nullError_throwsArgumentNullException() =>
        Assert.That(() => Result.Failure<Pence>(null!), Throws.TypeOf<ArgumentNullException>());

    [Test]
    public void SuccessOfT_nullValue_throwsArgumentNullException() =>
        Assert.That(() => Result.Success<string>(null!), Throws.TypeOf<ArgumentNullException>());

    [Test]
    public void ToResult_failure_keepsError()
    {
        Result<Pence> typed = Result.Failure<Pence>(_sample);

        Result untyped = typed.ToResult();

        Assert.That(untyped.IsFailure, Is.True);
        Assert.That(untyped.Error, Is.EqualTo(_sample));
    }

    [TestCase(ErrorCategory.Validation)]
    [TestCase(ErrorCategory.NotFound)]
    [TestCase(ErrorCategory.Conflict)]
    [TestCase(ErrorCategory.Unavailable)]
    public void Error_eachCategory_isKeptOnTheError(ErrorCategory category)
    {
        var error = new Error("some.code", "Something went wrong.", category);

        Assert.That(error.Category, Is.EqualTo(category));
        Assert.That(Result.Failure(error).Error.Category, Is.EqualTo(category));
    }

    [Test]
    public void ErrorCategory_definedValues_areExactlyTheFourDecided() =>
        Assert.That(
            Enum.GetNames<ErrorCategory>(),
            Is.EquivalentTo(_decidedCategories));

    [TestCase("")]
    [TestCase("   ")]
    public void Error_blankCode_throwsArgumentException(string code) =>
        Assert.That(() => new Error(code, "Message.", ErrorCategory.Validation), Throws.InstanceOf<ArgumentException>());

    [TestCase("")]
    [TestCase("   ")]
    public void Error_blankMessage_throwsArgumentException(string message) =>
        Assert.That(() => new Error("code", message, ErrorCategory.Validation), Throws.InstanceOf<ArgumentException>());

    [Test]
    public void Error_undefinedCategory_throwsArgumentOutOfRangeException() =>
        Assert.That(() => new Error("code", "Message.", (ErrorCategory)99), Throws.TypeOf<ArgumentOutOfRangeException>());

    [Test]
    public void Error_created_keepsCodeAndMessage()
    {
        Assert.That(_sample.Code, Is.EqualTo("input.missing"));
        Assert.That(_sample.Message, Is.EqualTo("A required figure is missing."));
    }

    [Test]
    public void Error_sameParts_areEqual()
    {
        var first = new Error("a", "b", ErrorCategory.Conflict);
        var second = new Error("a", "b", ErrorCategory.Conflict);

        Assert.That(first, Is.EqualTo(second));
    }

    [Test]
    public void ToResult_successWithAValue_isASuccess() =>
        Assert.That(Result.Success(new Pence(1)).ToResult().IsSuccess, Is.True);

    [Test]
    public void ToResult_failure_keepsTheError()
    {
        Result result = Result.Failure<Pence>(_sample).ToResult();

        Assert.That(result.IsFailure, Is.True);
        Assert.That(result.Error, Is.EqualTo(_sample));
    }
}
