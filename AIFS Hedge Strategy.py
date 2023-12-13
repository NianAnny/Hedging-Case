import pandas as pd

# Given data
volume = 10000
cost_per_participant = 1000  # Assuming this is in EUR
forward_rate = 1.2344  # 2-year forward rate
option_strike = forward_rate  # Assuming the strike price is the same as the forward rate
option_premium = 0.05  # Premium for the option
exchange_rates = {
    'Stable (0-Impact)': 1.22,  # USD/EUR exchange rate for zero impact scenario
    'Strong Dollar': 1.01,  # USD/EUR exchange rate for strong dollar scenario
    'Weak Dollar': 1.48  # USD/EUR exchange rate for weak dollar scenario
}

# If no hedging
def calculate_financial_impact(volume, cost_per_participant, exchange_rates):
    # Calculate the "zero impact" cost in USD
    zero_impact_cost = volume * cost_per_participant * exchange_rates['Stable (0-Impact)']

    # Calculate the total cost and impact for each scenario
    outcomes = {}
    for scenario, rate in exchange_rates.items():
        total_cost_usd = volume * cost_per_participant * rate
        windfall = total_cost_usd - zero_impact_cost
        impact = None  # Default to None
        if windfall < 0:
            impact = 'Positive'
        elif windfall > 0:
            impact = 'Negative'
        outcomes[scenario] = {
            'Total Cost USD': total_cost_usd,
            'Saving/Loss USD': windfall,
            'Impact': impact
        }
    return outcomes

# Calculate the financial impact without hedging
No_Hedging = calculate_financial_impact(volume, cost_per_participant, exchange_rates)

# Convert the outcomes to a pandas DataFrame for a tabular representation
df_outcomes = pd.DataFrame(No_Hedging).T  # Transpose for better formatting
df_outcomes.index.name = 'No-Hedging Scenario'
df_outcomes.reset_index(inplace=True)
df_outcomes.fillna('-', inplace=True)  # Replace NaN with '-' for presentation
print(f"{exchange_rates}")
print(df_outcomes)
######################################################

# Define the function to calculate the outcomes for hedging with forwards and options.
def calculate_hedging_outcomes(volume, cost_per_participant, exchange_rates, forward_rate, option_strike, option_premium):
    results = {'No Hedging': {}, '100% Forward Hedge': {}, '100% Option Hedge': {}}

    zero_impact_cost = volume * cost_per_participant * exchange_rates['Stable (0-Impact)']

    for scenario, rate in exchange_rates.items():
        no_hedging_cost = volume * cost_per_participant * rate
        results['No Hedging'][scenario] = no_hedging_cost

        # Hedging with forwards, the cost is locked at the forward rate.
        cost_hedge_forward = volume * cost_per_participant * forward_rate
        results['100% Forward Hedge'][scenario] = cost_hedge_forward

        # Hedging with options, exercise the option only if the spot rate is less than the strike rate.
        effective_rate = min(rate, option_strike)
        cost_hedge_option = volume * cost_per_participant * effective_rate
        option_total_cost = cost_hedge_option + (zero_impact_cost * option_premium)
        results['100% Option Hedge'][scenario] = option_total_cost

    return results

# Calculate the hedging outcomes
hedging_outcomes = calculate_hedging_outcomes(volume, cost_per_participant, exchange_rates, forward_rate, option_strike,
                                              option_premium)

# Convert the results to a pandas DataFrame for display
df = pd.DataFrame.from_dict(hedging_outcomes)
df.index.name = f"{forward_rate} USD/EUR"
df.reset_index(inplace=True)
print(f"\n{df}")
###############################################################################

# Define a function to calculate the outcomes of a 100% hedge with forwards and options.
# The function will return the net exposure in USD after hedging for both forwards and options.
def calculate_hedge_outcomes(forward_rate, option_strike, option_premium, revenue_eur, cost_eur, sales_volume,
                             zero_impact_sales):
    # Hedging with forwards
    hedged_revenue_forward = revenue_eur * forward_rate
    hedged_cost_forward = cost_eur * forward_rate
    net_exposure_forward = (hedged_revenue_forward - hedged_cost_forward) * sales_volume

    # Hedging with options
    # For options, consider the strike price only if it's beneficial to exercise the option.
    # (buy call if spot < strike, buy put if spot > strike), we use the spot.
    # We also need to account for the option premium paid.
    if option_strike > forward_rate:
        effective_option_rate = min(forward_rate, option_strike)
    else:
        effective_option_rate = max(forward_rate, option_strike)

    hedged_revenue_option = (revenue_eur * effective_option_rate) - (option_premium * revenue_eur)
    hedged_cost_option = (cost_eur * effective_option_rate) + (option_premium * cost_eur)
    net_exposure_option = (hedged_revenue_option - hedged_cost_option) * sales_volume

    return {
        "net_exposure_forward": net_exposure_forward,
        "net_exposure_option": net_exposure_option
    }

# Parameters
forward_rate = 1.2344  # 2-year forward rate
option_strike = forward_rate  # Assuming the strike price is the same as the forward rate
option_premium = 0.05  # Premium for the option
revenue_eur = 5000  # Revenue in EUR
cost_eur = 1000  # Cost in EUR
sales_volume = 25000  # Forecast of final sales volume
zero_impact_sales = 25000 # Assuming 25000 is the base volume for zero impact

# Calculate outcomes
outcomes = calculate_hedge_outcomes(forward_rate, option_strike, option_premium, revenue_eur, cost_eur, sales_volume,
                                    zero_impact_sales)
print(f"\n{outcomes}")
#############################################