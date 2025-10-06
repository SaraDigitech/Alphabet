import React from "react";

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, info) {
    console.error("Error caught by ErrorBoundary:", error);
    console.error("Component stack:", info.componentStack);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div
          style={{
            padding: "20px",
            textAlign: "center",
            color: "#fff",
            backgroundColor: "#d32f2f",
            borderRadius: "8px",
            margin: "20px",
          }}
        >
          <h1>Something went wrong. Please try again later.</h1>
          <code>
            We apologize for the inconvenience. If you continue to experience
            issues, please contact our support team at{" "}
            <a href="mailto:alphabet">alphabet.com</a>.
          </code>
        </div>
      );
    }


    return this.props.children;
  }
}

export default ErrorBoundary;
