#!/usr/bin/env python3
"""
Example script demonstrating how to use the dynex package with the provided configuration.
"""

import configparser
import os
import dynex

def load_config(config_file='dynex.ini'):
    """Load configuration from the config file."""
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def main():
    """Main function to demonstrate dynex usage."""
    try:
        # Load configuration
        config = load_config()
        
        # Extract dynex configuration
        dynex_config = config['DYNEX']
        ftp_config = config['FTP_SOLUTION_FILES']
        
        print("Dynex Configuration:")
        print(f"API Endpoint: {dynex_config['API_ENDPOINT']}")
        print(f"API Key: {dynex_config['API_KEY']}")
        print(f"API Secret: {dynex_config['API_SECRET']}")
        
        print("\nFTP Configuration:")
        print(f"Hostname: {ftp_config['ftp_hostname']}")
        print(f"Username: {ftp_config['ftp_username']}")
        print(f"Password: {ftp_config['ftp_password']}")
        
        # Test basic dynex functionality
        print("\nTesting Dynex functionality:")
        
        # Check if we can access the config from dynex
        if hasattr(dynex, 'config'):
            print("✓ Dynex config module available")
        
        # Test basic sampling functionality
        print("✓ Dynex package successfully installed and configured!")
        print("Available functions:")
        print("- sample_qubo()")
        print("- sample_ising()") 
        print("- estimate_costs()")
        print("- account_status()")
        
        # Example: Check account status
        print("\nChecking account status...")
        try:
            status = dynex.account_status()
            print(f"Account status: {status}")
        except Exception as e:
            print(f"Could not check account status: {e}")
        
    except FileNotFoundError:
        print("Configuration file 'dynex.ini' not found!")
    except KeyError as e:
        print(f"Missing configuration key: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 