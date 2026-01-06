# P&L Calendar

## Overview
This project is a application that tracks daily profits and losses in the stock market using a calendar with heatmap coloring. It was built with Python and Tkinter.

This program is designed to simply track trades made in the stock market with a clean and simple UI, making it ideal for beginner traders.

## Features
* Monthly calendar view (Mon-Sun)
* Heatmap Coloring
   - Green for positive numbers
   - Red for negative numbers
   - Color intensity is scaled relative to the largest absolute PnL in that month
* Click on date to enter a profit or loss (positive or negative number)
* Data stored locally in .json file
* Statistics
   - Monthly total
   - Average (filled days only)
   - Win rate
* Input number parsing
   - Allows: +100, -100, 100, (100), -$100, $100
* CSV import/export
* Button to jump to today's date
* Button to clear months profits and losses

## Requirements
* Python 3.9+

## Credit
* Inspired by Webull's P&L calendar UI



