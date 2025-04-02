import streamlit as st

st.set_page_config(page_title="Math Tool Home", layout="wide")

st.title("Interactive Math")
st.subheader("seperet.com")

st.markdown("""
This application provides interactive tools to quickly visualize Algebra, Geometry, Trig, and Calculus.

**👈 Select a module from the sidebar to get started.**

Here's a brief overview of the available modules:

* **📐 Trigonometry Workbench:** Explore the unit circle, graph trig functions, work with identities, and solve equations.
* **🔺 Triangle Solver & Applications:** Solve triangles (SSS, SAS, etc.) and visualize geometric problems like bearings and angles of elevation/depression.
* **📈 Functions & Algebra:** Plot functions, analyze basic properties, and work with logarithmic/exponential expressions.
* **Σ Calculus 1: Limits & Derivatives:** Calculate limits and derivatives, and visualize tangent lines.
* **∫ Calculus 2: Integration:** Compute definite and indefinite integrals, and visualize area under curves.
* **♾️ Calculus 2: Sequences & Series:** Explore sequences and Taylor series approximations (more features coming soon).
* **🛠️ General Tools:** Simplify expressions and verify mathematical equality.

**Tips for Use:**

* Use standard mathematical notation (e.g., `x^2`, `sin(x)`, `log(x, 10)`, `exp(x)`).
* Common variables like `x, y, z, t, theta` and constants `a, b, c, k` are usually pre-defined.
* Check the specific instructions within each module.
* Calculations involving symbolic math (like simplification or integration) can sometimes take a few seconds.

*Developed using Streamlit, SymPy, Plotly, and NumPy.*
""")