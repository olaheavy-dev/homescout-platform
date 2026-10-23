namespace HomeScout.CostEngine;

/// <summary>
/// The outcome of an operation that can fail for an expected reason (invalid input, not found, an unavailable source).
/// Programming errors throw instead (decisions 0021, 0032).
/// </summary>
public sealed class Result
{
    private readonly Error? _error;

    private Result(Error? error) => _error = error;

    /// <summary>Whether the operation worked.</summary>
    public bool IsSuccess => _error is null;

    /// <summary>Whether the operation failed.</summary>
    public bool IsFailure => _error is not null;

    /// <summary>The failure. Reading it on a success is a programming error and throws.</summary>
    /// <exception cref="InvalidOperationException">The result is a success.</exception>
    public Error Error => _error ?? throw new InvalidOperationException("A successful result has no error.");

    /// <summary>A success.</summary>
    public static Result Success() => new(null);

    /// <summary>A failure carrying <paramref name="error"/>.</summary>
    public static Result Failure(Error error)
    {
        ArgumentNullException.ThrowIfNull(error);
        return new Result(error);
    }

    /// <summary>A success carrying <paramref name="value"/>.</summary>
    public static Result<T> Success<T>(T value)
        where T : notnull
    {
        ArgumentNullException.ThrowIfNull(value);
        return new Result<T>(value, null);
    }

    /// <summary>A failure carrying <paramref name="error"/>, for an operation that would have produced a <typeparamref name="T"/>.</summary>
    public static Result<T> Failure<T>(Error error)
        where T : notnull
    {
        ArgumentNullException.ThrowIfNull(error);
        return new Result<T>(default, error);
    }
}

/// <summary>A <see cref="Result"/> that carries a value when it succeeds.</summary>
/// <typeparam name="T">The value type. Never null.</typeparam>
public sealed class Result<T>
    where T : notnull
{
    private readonly T? _value;
    private readonly Error? _error;

    internal Result(T? value, Error? error)
    {
        _value = value;
        _error = error;
    }

    /// <summary>Whether the operation worked.</summary>
    public bool IsSuccess => _error is null;

    /// <summary>Whether the operation failed.</summary>
    public bool IsFailure => _error is not null;

    /// <summary>The value. Reading it on a failure is a programming error and throws.</summary>
    /// <exception cref="InvalidOperationException">The result is a failure.</exception>
    public T Value => _error is null
        ? _value!
        : throw new InvalidOperationException("A failed result has no value.");

    /// <summary>The failure. Reading it on a success is a programming error and throws.</summary>
    /// <exception cref="InvalidOperationException">The result is a success.</exception>
    public Error Error => _error ?? throw new InvalidOperationException("A successful result has no error.");

    /// <summary>Drops the value, keeping only success or the error.</summary>
    public Result ToResult() => _error is null ? Result.Success() : Result.Failure(_error);
}
