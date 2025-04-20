import streamlit as st
import pandas as pd

st.set_page_config(page_title="SKU Mapper", layout="wide")

st.title("📦 SKU to MSKU Mapper - WMS Tool")

# we can upload Sales Data for SKU Mapping
st.header("Step 1: Upload Sales Data")
sales_file = st.file_uploader("Upload Sales Data CSV", type=["csv"], key="sales")

# we can upload SKU Mapping File for SKU Mapping
st.header("Step 2: Upload SKU to MSKU Mapping File")
mapping_file = st.file_uploader("Upload Mapping File CSV", type=["csv"], key="mapping")

# we can show sales data preview for display to user
if sales_file:
    try:
        sales_df = pd.read_csv(sales_file)

        sales_df.columns = sales_df.columns.str.strip().str.lower()

        st.subheader("🔍 Sales Data Preview")
        st.dataframe(sales_df.head())

        st.text("Sales Columns: " + ", ".join(sales_df.columns))
    except Exception as e:
        st.error(f"❌ Error reading sales file: {e}")

# we can show mapping file preview for display to user
if mapping_file:
    try:
        mapping_df = pd.read_csv(mapping_file)

        mapping_df.columns = mapping_df.columns.str.strip().str.lower()

        mapping_df.rename(columns={
            "master_sku": "msku",
            "sku_code": "sku"
        }, inplace=True)

        st.subheader("🔍 SKU Mapping Preview")
        st.dataframe(mapping_df.head())

        st.text("Mapping Columns: " + ", ".join(mapping_df.columns))

    except Exception as e:
        st.error(f"❌ Error reading mapping file: {e}")

if sales_file and mapping_file:
    if st.button("🔁 Map SKUs to MSKUs"):
        try:
            sku_dict = dict(zip(mapping_df["sku"], mapping_df["msku"]))
            sales_df["msku"] = sales_df["sku"].map(sku_dict)

            st.success("✅ Mapping complete!")
            st.subheader("📋 Mapped Sales Data")
            st.dataframe(sales_df)

            csv = sales_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Mapped Data as CSV",
                data=csv,
                file_name="mapped_sales_data.csv",
                mime="text/csv",
            )

        except Exception as e:
            st.error(f"❌ Error during mapping: {e}")

st.header("📥 Upload All CSV Files")

inventory_file = st.file_uploader("1️⃣ Upload Current Inventory CSV", type=["csv"], key="inv")

mapping_file = st.file_uploader("2️⃣ Upload MSKU With SKUs CSV", type=["csv"], key="map")

combo_file = st.file_uploader("3️⃣ Upload Combos SKUs CSV", type=["csv"], key="combo")

if inventory_file:
    try:
        inventory_df_raw = pd.read_csv(inventory_file, header=None)
        st.subheader("📦 Current Inventory - Raw Preview")
        st.dataframe(inventory_df_raw.head(10))

        if st.checkbox("Use first row as header for Inventory?"):
            inventory_df_raw.columns = inventory_df_raw.iloc[0]
            inventory_df = inventory_df_raw[1:].reset_index(drop=True)
        else:
            inventory_df = inventory_df_raw

        inventory_df.columns = inventory_df.columns.astype(str).str.strip().str.lower()
        st.text("Inventory Columns: " + ", ".join(inventory_df.columns))

    except Exception as e:
        st.error(f"❌ Error reading inventory file: {e}")

if mapping_file:
    mapping_df = pd.read_csv(mapping_file)
    mapping_df.columns = mapping_df.columns.str.strip().str.lower()
    mapping_df.rename(columns={"product": "msku"}, inplace=True)  # adjust if needed
    st.subheader("🔗 MSKU Mapping Preview")
    st.dataframe(mapping_df.head())
    st.text("Mapping Columns: " + ", ".join(mapping_df.columns))

if combo_file:
    combo_df = pd.read_csv(combo_file)
    combo_df.columns = combo_df.columns.str.strip().str.lower()
    st.subheader("🧩 Combo SKUs Preview")
    st.dataframe(combo_df.head())
    st.text("Combo Columns: " + ", ".join(combo_df.columns))
