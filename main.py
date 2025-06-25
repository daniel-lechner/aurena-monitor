#!/usr/bin/env python3
"""
Aurena Auction Monitor - Main CLI Interface
"""

import sys
import inquirer

def show_banner():
    """Display application banner"""
    print("🏆 Aurena Auction Monitor")
    print("=" * 30)
    print()

def run_auction_fetch():
    """Run the auction fetching process"""
    try:
        from fetch.auction_monitor import AurenaMonitor
        monitor = AurenaMonitor()
        monitor.run()
    except ImportError as e:
        print(f"❌ Error importing: {e}")
        input("Press Enter to continue...")

def main():
    """Main application entry point"""
    while True:
        show_banner()
        
        questions = [
            inquirer.List('action',
                         message="What would you like to do?",
                         choices=[
                             '🔍 Fetch auction data',
                             '❌ Exit'
                         ])
        ]
        
        answers = inquirer.prompt(questions)
        
        if not answers:  # User pressed Ctrl+C
            break
            
        if answers['action'] == '🔍 Fetch auction data':
            print()
            run_auction_fetch()
        elif answers['action'] == '❌ Exit':
            print("👋 Goodbye!")
            break
        
        print()

if __name__ == "__main__":
    main()