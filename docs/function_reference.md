# Function Reference

## Overview

This document provides a reference for all major functions in the project. Each entry includes the function signature, description, parameters, return values, examples, and related functions.

## Table of Contents

Module: api_library

Module: utils

### Module: api_library

**Class: PullData**

{

def get_market_data(self, page: int = 1) -> pd.DataFrame

* Gets the current market data for a list of 100 cryptocurrencies. Changing page allows viewing of different lists.

def get_crypto_details(self, crypto_id: str) -> Dict

* Gets the crypto details of a single crypto

**Parameters**

    crypto_id       str     The name of a cryptocurrency

**Returns**

A pandas dataframe

**List of available keys**

    'id'
    'symbol'
    'name'
    'description'
    'current_price'
    'market_cap'
    'total_volume'
    'price_change_24h'
    'all_time_high'
    'all_time_low'
    'homepage'

**Example:**

    dataPuller = PullData()
    btc_details = dataPuller.get_crypto_details('bitcoin')
    print(f"Name: {btc_details['name']}")

Returns: 

    "Name: Bitcoin"



def get_historical_data(self, crypto_id: str, days: int = 30) -> pd.DataFrame

* 

def get_current_price(self, crypto_ids: List[str], vs_currency: str = "usd") -> Dict

* 

}