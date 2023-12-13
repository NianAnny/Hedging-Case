import pandas as pd 

# Constants provided
forecasted_sales_units = 32750
average_sales_price_usd = 90000
cost_per_vehicle_eur = 60000
expected_spot_rate = 1.42
forward_rate = 1.45
option_strike = forward_rate
premium = 0.05

# Hedging strategy proportions
mixed_forward = 0.7  # Proportion hedged with forwards
mixed_option = 0.7   # Proportion hedged with options 
alternative_forward = 0.5  # Proportion hedged with forwards in alternative strategy
alternative_option = 1 - alternative_forward  # Remaining proportion hedged with options in alternative strategy

total_revenue_usd = forecasted_sales_units * average_sales_price_usd
total_costs_eur = forecasted_sales_units * cost_per_vehicle_eur

finance_cost_forward = total_revenue_usd / expected_spot_rate - total_revenue_usd / forward_rate
finance_cost_options = forecasted_sales_units * premium

inflow_forwards = total_revenue_usd / forward_rate
option_stike = min(option_strike, expected_spot_rate)
inflow_options = total_revenue_usd / option_strike - finance_cost_options

profit_forwards = inflow_forwards - total_costs_eur - finance_cost_forward
profit_options = inflow_options - total_costs_eur 

print(finance_cost_forward, finance_cost_options)


# Scenarios and their corresponding multipliers
scenarios = ['As Forecasted', '30% Below Forecast', '30% Above Forecast']
multipliers = [1, 0.7, 1.3]

# DataFrame to store results
results_df = pd.DataFrame(index=scenarios, columns=['Sales Amount', 
                                                    'No Hedge', 
                                                    '100% Hedge with Forwards', 
                                                    '100% Hedge with Options', 
                                                    '70% Hedge with Forwards, 30% No Hedge', 
                                                    '70% Hedge with Options, 30% No Hedge',
                                                    '50% Hedge with Forwards, 50% Hedge with Options'])

# Calculate the gross profit in EUR for each scenario and hedging strategy
for scenario, multiplier in zip(scenarios, multipliers):
    sales_volume = forecasted_sales_units * multiplier
    revenue_usd = sales_volume * average_sales_price_usd
    costs_eur = sales_volume * cost_per_vehicle_eur
    
    
    # expected_spot_rate is smaller, no premium effects
    option_strike = min(option_strike, expected_spot_rate)
    
    # No hedge scenario: convert USD revenue to EUR at expected spot rate
    results_df.at[scenario, 'Sales Amount'] = sales_volume
    results_df.at[scenario, 'No Hedge'] = revenue_usd / expected_spot_rate - costs_eur
    
    
    # 100% Hedge with forwards: convert USD revenue to EUR at forward rate
    results_df.at[scenario, '100% Hedge with Forwards'] = revenue_usd / forward_rate - costs_eur
    
    # 100% Hedge with options: convert USD revenue to EUR at option strike rate plus premium
    results_df.at[scenario, '100% Hedge with Options'] = revenue_usd / (option_strike) - costs_eur

    # Mixed hedge with forwards: partially convert costs at forward rate, rest at spot rate
    results_df.at[scenario, '70% Hedge with Forwards, 30% No Hedge'] = (revenue_usd * mixed_forward / forward_rate + 
                                                                         revenue_usd * (1 - mixed_forward) / expected_spot_rate) - costs_eur
    
    # Mixed hedge with options: partially convert costs at option strike rate with premium, rest at spot rate
    results_df.at[scenario, '70% Hedge with Options, 30% No Hedge'] = (revenue_usd * mixed_option / (option_strike) + 
                                                                       revenue_usd * (1 - mixed_option) / expected_spot_rate) - costs_eur
    
    # Alternative hedge: split the hedge between forwards and options
    results_df.at[scenario, '50% Hedge with Forwards, 50% Hedge with Options'] = ((revenue_usd * alternative_forward / forward_rate) + 
                                                                                   (revenue_usd * alternative_option / (option_strike))) - costs_eur

results_df = results_df.astype(float).round(0).T
print(results_df)
