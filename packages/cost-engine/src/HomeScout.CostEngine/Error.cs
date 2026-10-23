using System.Diagnostics.CodeAnalysis;

namespace HomeScout.CostEngine;

/// <summary>The kind of an expected failure, so the API can later map each to a standard response in one place (decision 0032).</summary>
public enum ErrorCategory
{
    /// <summary>The input is invalid or incomplete.</summary>
    Validation,

    /// <summary>Something asked for does not exist.</summary>
    NotFound,

    /// <summary>The request clashes with the current state.</summary>
    Conflict,

    /// <summary>An outside service or data source could not be used.</summary>
    Unavailable,
}

/// <summary>
/// Why an expected operation failed: a stable code for programs, a plain-language message for people, and a category.
/// </summary>
[SuppressMessage(
    "Naming",
    "CA1716:Identifiers should not match keywords",
    Justification = "Decision 0032 names this type Error. Only Visual Basic reserves the word, and HomeScout is C# only.")]
public sealed record Error
{
    public Error(string code, string message, ErrorCategory category)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(code);
        ArgumentException.ThrowIfNullOrWhiteSpace(message);

        if (!Enum.IsDefined(category))
        {
            throw new ArgumentOutOfRangeException(nameof(category), category, "Unknown error category.");
        }

        Code = code;
        Message = message;
        Category = category;
    }

    /// <summary>A stable identifier such as <c>input.missing</c>. Tests and callers match on this, never on the message.</summary>
    public string Code { get; }

    /// <summary>A plain-language explanation that can be shown to a person.</summary>
    public string Message { get; }

    /// <summary>The kind of failure.</summary>
    public ErrorCategory Category { get; }
}
