# Shark Tank India Season 1 — Investment Analysis  
### A Complete End-to-End Data Analytics Project using Python

This project is a deep-dive analysis into investment patterns, founder asks, valuations, and shark behaviour from **Shark Tank India (Season 1)**.  
Using the full dataset from the show, the project uncovers trends that influence whether a pitch secures a deal, how sharks negotiate, and what factors drive valuation decisions.


---

## Objectives

- Understand which types of startups get funded  
- Analyse shark participation and investment style  
- Study deal structures (amount, equity, valuation)  
- Identify episode-wise funding trends  
- Compare founder asks vs. final deal outcomes  
- Compute ROI for each shark  

---

## Data Cleaning Summary

The dataset required significant preprocessing:

- Normalized column names  
- Removed duplicates  
- Cleaned monetary fields by removing ₹, %, commas  
- Converted equity, amount, valuation fields to numeric  
- Created a unified `deal_flag` column  
- Fixed inconsistent datatypes across the sheet  

All cleaning was done programmatically using **Pandas**.

---

## Key Insights

### Deal Conversion  
- Total Pitches: **119**  
- Successful Deals: **65**  
- Deal Success Rate: **~54%**

### Shark Behaviour  
- Several sharks showed distinct investing personalities  
- A bar chart highlights the top 3 most active investors  
- Multi-shark deals occur less often than expected  

### Money & Equity  
- Median deal amount paints a clearer picture than average  
- Equity asks vary widely, with a few extreme outliers  
- Episode-wise equity trends reveal negotiation patterns  

### Ask vs. Deal Relationship  
- Moderate ask amounts correlate with higher deal success  
- Some founders receive higher deal amounts than their ask  

### ROI Analysis  
A simple ROI metric (equity gained per rupee invested) ranks sharks by negotiation strength.

---

## Visualisations

The project includes:

- Deal amount boxplots  
- Equity distribution boxplots  
- Episode-wise deal trend line charts  
- Top-shark bar charts  
- Scatter plots for valuation and ask relationships  
- ROI comparison graphs  

All visuals are stored in the `Visuals/` folder.

---

## Technologies Used

- **Python**
- **Pandas**
- **NumPy**
- **Matplotlib**
---