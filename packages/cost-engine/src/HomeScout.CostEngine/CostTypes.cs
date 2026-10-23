namespace HomeScout.CostEngine;

/// <summary>How often an amount is charged, as its source states it.</summary>
public enum Period
{
    /// <summary>One time only.</summary>
    Once,

    /// <summary>Every month.</summary>
    Month,

    /// <summary>Every year.</summary>
    Year,
}

/// <summary>Whether a home is being bought or rented.</summary>
public enum Mode
{
    /// <summary>Buying.</summary>
    Buy,

    /// <summary>Renting.</summary>
    Rent,
}

/// <summary>A kind of cost the engine knows how to place in a monthly or upfront breakdown.</summary>
public enum CostCategory
{
    /// <summary>The monthly mortgage payment.</summary>
    MortgageRepayment,

    /// <summary>A leasehold service charge.</summary>
    ServiceCharge,

    /// <summary>A leasehold ground rent.</summary>
    GroundRent,

    /// <summary>Council tax.</summary>
    CouncilTax,

    /// <summary>Energy bills.</summary>
    Energy,

    /// <summary>Water bills.</summary>
    Water,

    /// <summary>Broadband.</summary>
    Broadband,

    /// <summary>Buildings insurance.</summary>
    BuildingsInsurance,

    /// <summary>Maintenance.</summary>
    Maintenance,

    /// <summary>The monthly rent.</summary>
    Rent,

    /// <summary>The deposit towards a purchase.</summary>
    MortgageDeposit,

    /// <summary>A tenancy deposit.</summary>
    Deposit,

    /// <summary>The first month's rent, paid up front.</summary>
    FirstMonthRent,

    /// <summary>The cost of moving.</summary>
    MovingCosts,

    /// <summary>Stamp duty.</summary>
    StampDuty,

    /// <summary>Legal fees.</summary>
    LegalFees,
}

/// <summary>What a cost line is in a result: an amount, or the reason there is no amount.</summary>
public enum LineStatus
{
    /// <summary>The engine worked out an amount.</summary>
    Calculated,

    /// <summary>Covered by another charge (for example water included in the rent). It adds nothing.</summary>
    Included,

    /// <summary>This version does not work it out. It adds nothing and makes the total partial.</summary>
    NotCalculated,

    /// <summary>Sources disagree and it is not settled. It adds nothing and makes the total partial.</summary>
    Conflicting,

    /// <summary>There is no evidence for it. It adds nothing and makes the total partial.</summary>
    Missing,
}
