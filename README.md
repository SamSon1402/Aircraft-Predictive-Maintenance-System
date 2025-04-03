# Aircraft Predictive Maintenance System

![Image](https://github.com/user-attachments/assets/522998ac-f276-4345-83f4-cce5b8654acc)

![Image](https://github.com/user-attachments/assets/23d0fc5e-bea7-42f5-86ab-26980519fa66)

![Image](https://github.com/user-attachments/assets/46ed4604-a053-42ec-bc10-20233541d72e)

![Image](https://github.com/user-attachments/assets/3005e4c0-748b-4012-b221-6dabcf88d275)

![Image](https://github.com/user-attachments/assets/5fd2e988-84e2-4d9b-9d15-bab81f5c789e)

![Image](https://github.com/user-attachments/assets/49c09131-76fc-4879-8833-cda79c3353c2)



## Business Value for SITA

This Predictive Maintenance System directly supports SITA's mission to optimize airline operations and reduce the aviation sector's environmental impact through AI-powered solutions.

### How This System Helps SITA's Business

#### 1. Cost Reduction
- **Unscheduled vs. Scheduled Maintenance**: Saves approximately $175,000 per event by shifting from emergency repairs to planned maintenance
- **Extended Component Life**: Maximizes the useful life of aircraft components while ensuring safety
- **Reduced Inventory Costs**: Better predictions mean optimized spare parts inventory

#### 2. Operational Improvements
- **Decreased Delays**: Fewer unexpected mechanical issues means fewer flight cancellations and delays
- **Improved Resource Planning**: Maintenance staff and resources can be scheduled efficiently
- **Enhanced Fleet Management**: Better visibility into the health of the entire fleet

#### 3. Environmental Impact
- **Reduced Fuel Consumption**: Properly maintained engines are more fuel-efficient
- **Lower CO₂ Emissions**: The sustainability calculator demonstrates significant emission reductions
- **Support for SITA's Green Initiatives**: Aligns with SITA's commitment to environmental responsibility

#### 4. Competitive Advantage
- **Value-Added Service**: SITA can offer this as a premium solution to airline clients
- **Data-Driven Decision Making**: Provides airlines with actionable insights, not just raw data
- **Industry Leadership**: Positions SITA at the forefront of aviation technology innovation

## Key Features

- **Dashboard**: Real-time fleet status with critical maintenance alerts
- **Analysis Tools**: Deep dive into engine sensor data and degradation patterns
- **Predictive Engine**: Machine learning-powered Remaining Useful Life (RUL) predictions
- **Sustainability Calculator**: Quantifies environmental benefits of preventive maintenance

## Technical Implementation

### Tech Stack
- **Frontend**: Streamlit for interactive web interface
- **Data Processing**: Pandas and NumPy for data manipulation
- **Visualization**: Plotly for interactive charts and graphs
- **Machine Learning**: Scikit-learn for predictive modeling
- **Styling**: Custom CSS for enhanced user experience

### Machine Learning Approach
This system uses a **Random Forest Regressor** model for predicting Remaining Useful Life (RUL). This model was chosen because it:

- Handles the non-linear relationships in sensor data
- Provides reliable predictions even with noisy data
- Offers built-in feature importance analysis
- Requires minimal hyperparameter tuning
- Performs well with the available amount of data

The model analyzes patterns from multiple aircraft sensors, identifies degradation trends, and predicts when maintenance will be needed before failures occur.

## Potential Business Expansion

This system can be extended to support SITA's business growth through:

1. **Cross-fleet analytics**: Compare performance across different aircraft types
2. **Maintenance workflow integration**: Connect with existing maintenance systems
3. **Mobile applications**: Provide on-the-go access for maintenance crews
4. **API services**: Allow integration with airline-specific systems

---

Developed for SITA's Data Intelligence Team to enhance their AI-powered solutions for the aviation industry, with a specific focus on reducing operational costs and environmental impact.
