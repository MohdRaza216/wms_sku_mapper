import streamlit as st
import pandas as pd

st.set_page_config(page_title="SKU Mapper", layout="wide")

st.title("📦 SKU to MSKU Mapper - WMS Tool")

# Upload Sales Data
st.header("Step 1: Upload Sales Data")
sales_file = st.file_uploader("Upload Sales Data CSV", type=["csv"], key="sales")

# Upload SKU Mapping File
st.header("Step 2: Upload SKU to MSKU Mapping File")
mapping_file = st.file_uploader("Upload Mapping File CSV", type=["csv"], key="mapping")

# Show sales data preview
if sales_file:
    try:
        sales_df = pd.read_csv(sales_file)
        st.subheader("🔍 Sales Data Preview")
        if st.checkbox("Show full Sales Data"):
            st.dataframe(sales_df)
        else:
            st.dataframe(sales_df.head())

    except Exception as e:
        st.error(f"❌ Error reading sales file: {e}")

# Show mapping file preview
if mapping_file:
    try:
        mapping_df = pd.read_csv(mapping_file)
        st.subheader("🔍 SKU Mapping Preview")
        if st.checkbox("Show full Mapping Data"):
            st.dataframe(mapping_df)
        else:
            st.dataframe(mapping_df.head())

    except Exception as e:
        st.error(f"❌ Error reading mapping file: {e}")

# Step 3: Perform Mapping
if sales_file and mapping_file and st.button("🔁 Map SKUs to MSKUs"):
        try:
            sku_dict = dict(zip(mapping_df['sku'], mapping_df['msku']))
            sales_df['msku'] = sales_df['sku'].map(sku_dict)

            st.success("✅ Mapping complete!")
            st.subheader("📋 Mapped Sales Data")
            st.dataframe(sales_df)

            # Optional: Download the result as CSV
            csv = sales_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Mapped Data as CSV",
                data=csv,
                file_name="mapped_sales_data.csv",
                mime="text/csv",
            )

        except Exception as e:
            st.error(f"❌ Error during mapping: {e}")
