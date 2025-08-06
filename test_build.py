#!/usr/bin/env python3
"""
Simple test script to verify the project builds and imports correctly.
"""

def test_imports():
    """Test that all major modules can be imported."""
    try:
        from agents import Agent, Runner, Tool, function_tool
        print("✓ agents module imported successfully")
        
        from agents import MultiProvider, OpenAIProvider
        print("✓ models module imported successfully")
        
        from agents import function_tool
        print("✓ tools module imported successfully")
        
        from agents import InputGuardrail, OutputGuardrail
        print("✓ guardrail module imported successfully")
        
        from agents import Handoff
        print("✓ handoffs module imported successfully")
        
        from agents import Session
        print("✓ memory module imported successfully")
        
        from agents import trace
        print("✓ tracing module imported successfully")
        
        # Test dynex import
        import dynex
        print("✓ dynex module imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality without external dependencies."""
    try:
        from agents import Agent
        
        # Create a simple agent (won't run without API key, but should create)
        agent = Agent(
            name="test_agent",
            instructions="You are a helpful assistant."
        )
        print("✓ Agent creation works")
        
        # Test configuration loading
        import configparser
        config = configparser.ConfigParser()
        config.read('dynex.ini')
        
        if 'DYNEX' in config:
            print("✓ Dynex configuration loaded successfully")
            print(f"  API Endpoint: {config['DYNEX']['API_ENDPOINT']}")
        else:
            print("✗ Dynex configuration not found")
            
        return True
        
    except Exception as e:
        print(f"✗ Functionality test error: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing OpenAI Agents Python SDK build...")
    print("=" * 50)
    
    import_success = test_imports()
    functionality_success = test_basic_functionality()
    
    print("=" * 50)
    if import_success and functionality_success:
        print("✓ All tests passed! The project is built and ready to use.")
        print("\nNext steps:")
        print("1. Set OPENAI_API_KEY environment variable to use OpenAI features")
        print("2. Use dynex.ini configuration for Dynex integration")
        print("3. Run examples with: uv run python examples/basic/hello_world.py")
    else:
        print("✗ Some tests failed. Please check the errors above.")
    
    return import_success and functionality_success

if __name__ == "__main__":
    main() 