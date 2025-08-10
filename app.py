# app.py
from flask import Flask, render_template, request, jsonify
import json
import os
import time

# Import your selenium functions
from selenium_helpers import (
    create_driver, 
    open_case_status, 
    fill_case_details, 
    check_data_and_click_orders, 
    get_orders_list
)

app = Flask(__name__)

def load_case_types():
    """Load case types from JSON file"""
    try:
        # Check if case_types.json exists
        if os.path.exists('case_types.json'):
            with open('case_types.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                # If it's a list, return it directly
                if isinstance(data, list):
                    return data
                # If it's a dict, try to get case types from it
                elif isinstance(data, dict):
                    return data.get('case_types', list(data.keys()))
        else:
            print("⚠️ case_types.json not found, using default case types")
            
    except Exception as e:
        print(f"⚠️ Error loading case_types.json: {e}")
    
    # Fallback to default case types if JSON loading fails
    return ["BAIL APPLN.", "CRIMINAL APPEAL", "CIVIL SUIT", "WRIT PETITION"]

@app.route('/')
def index():
    case_types = load_case_types()
    years = list(range(2020, 2026))
    
    print(f"✅ Loaded {len(case_types)} case types from JSON")
    return render_template('index.html', case_types=case_types, years=years)

@app.route('/search', methods=['POST'])
def search_case():
    try:
        # Get form data
        case_type = request.form.get('case_type')
        case_number = request.form.get('case_number')
        case_year = request.form.get('case_year')
        
        # Validate input
        if not case_type or not case_number or not case_year:
            return jsonify({
                'status': 'error',
                'message': 'All fields are required!'
            })
        
        print(f"🔍 Starting search for: {case_type}, Case #{case_number}, Year {case_year}")
        
        # Create selenium driver with shorter timeouts
        print("🚀 Creating driver...")
        driver = create_driver(headless=True)  
        print("✅ Driver created successfully")
        
        try:
            # Step 1: Open case status page
            print("📂 Opening case status page...")
            open_case_status(driver, timeout=20)  # Increased timeout
            print("✅ Case status page opened")
            time.sleep(2)
            
            # Step 2: Fill case details
            print("📝 Filling case details...")
            fill_case_details(driver, case_type, case_number, case_year, timeout=20)
            print("✅ Case details filled and submitted")
            time.sleep(3)
            
            # Step 3: Check data and click orders
            print("🔍 Checking search results...")
            result = check_data_and_click_orders(driver, wait_time=15)
            print(f"✅ Check result: {result}")
            
            if result["status"] == "no_data":
                return jsonify({
                    'status': 'no_data',
                    'message': 'No data found for the given case details.'
                })
            elif result["status"] == "orders_page":
                # Step 4: Get orders list
                print("📋 Extracting orders...")
                orders = get_orders_list(driver, wait_time=10)
                print(f"✅ Orders extracted: {len(orders)} found")
                
                if orders:
                    return jsonify({
                        'status': 'success',
                        'message': f'Found {len(orders)} orders',
                        'orders': orders
                    })
                else:
                    return jsonify({
                        'status': 'no_orders',
                        'message': 'Case found but no orders available.'
                    })
            else:
                return jsonify({
                    'status': 'error',
                    'message': f"Error checking results: {result.get('error', 'Unknown error')}"
                })
                
        except Exception as e:
            print(f"❌ Error during selenium operations: {str(e)}")
            return jsonify({
                'status': 'error',
                'message': f'Selenium error: {str(e)}'
            })
        finally:
            # Always close the driver
            print("🔒 Closing browser...")
            driver.quit()
            print("✅ Browser closed successfully")
            
    except Exception as e:
        print(f"❌ General error in search: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Search failed: {str(e)}'
        })

if __name__ == '__main__':
    app.run(debug=True, port=5000)