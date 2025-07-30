"""
TensorFlow Compatibility Helper for Streamlit Cloud
"""
import streamlit as st
import sys
import platform

def check_tensorflow_compatibility():
    """Check TensorFlow installation and compatibility"""
    st.header("🔧 TensorFlow Compatibility Check")
    
    st.write(f"**Python Version:** {sys.version}")
    st.write(f"**Platform:** {platform.platform()}")
    
    try:
        import tensorflow as tf
        st.success(f"✅ TensorFlow {tf.__version__} is available")
        
        # Check if GPU is available
        if tf.config.list_physical_devices('GPU'):
            st.info("🚀 GPU acceleration available")
        else:
            st.info("💻 Running on CPU")
            
        # Test basic operations
        try:
            x = tf.constant([[1.0, 2.0], [3.0, 4.0]])
            y = tf.constant([[1.0, 1.0], [0.0, 1.0]])
            result = tf.matmul(x, y)
            st.success("✅ TensorFlow operations working correctly")
        except Exception as e:
            st.error(f"❌ TensorFlow operation test failed: {e}")
            
    except ImportError as e:
        st.error(f"❌ TensorFlow not available: {e}")
        st.info("💡 Disease detection features will be disabled")
    
    try:
        import keras
        st.success(f"✅ Keras {keras.__version__} is available")
    except ImportError as e:
        st.error(f"❌ Keras not available: {e}")

if __name__ == "__main__":
    check_tensorflow_compatibility()
