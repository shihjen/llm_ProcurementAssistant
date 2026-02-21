import streamlit as st
import tempfile
import pandas as pd
from loaders.document_loaders import extract_text
from llm.schema_generator import generate_schema
from llm.model_builder import build_model
from llm.quotation_extractor import extract_quotation
from llm.evaluator import evaluate_vendor
from llm.recommender import recommend


st.title("Smart Procurement System")
st.sidebar.header("Upload Documents")

procurement_spec = st.sidebar.file_uploader(
    "Upload Procurement Specification",
    type=["pdf", "docx", "xlsx"]
)

if procurement_spec:

    text = extract_text(procurement_spec)

    st.subheader("📄 Extracted Specification")
    st.text_area("", text, height=250)

    if st.button("🧠 Analyze Specification"):
        with st.spinner("LLM analyzing requirements..."):
            schema = generate_schema(text)
            RequirementModel = build_model(schema)
            st.success("Requirement Model Generated ✅")
            st.session_state["schema"] = schema
            st.session_state["RequirementModel"] = RequirementModel
            st.subheader("Generated Schema")
            st.json(schema)
            st.subheader("Generated Pydantic Model")
            st.code(
                RequirementModel.model_json_schema(),
                language="json"
            )


if "schema" in st.session_state:
    quotation_files = st.sidebar.file_uploader(
        "Upload Vendor Quotations",
        accept_multiple_files=True,
        type=["pdf", "docx", "xlsx"]
    )
    if quotation_files:
        st.subheader("📊 Vendor Evaluation")
        evaluations = []
        table_rows = []
        for file in quotation_files:
            # save temporary file
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=file.name
            ) as tmp:

                tmp.write(file.getbuffer())
                filepath = tmp.name

            with st.spinner(f"Processing {file.name}..."):
                vendor_data = extract_quotation(
                    filepath,
                    st.session_state["schema"]
                )
                result = evaluate_vendor(
                    vendor_data,
                    st.session_state["schema"]
                )
                evaluations.append({
                    "vendor": vendor_data,
                    "evaluation": result
                })
                table_rows.append({
                    "Vendor": vendor_data.get("vendor", file.name),
                    "Score": result["score"],
                    "Total": result["total"],
                    "Compliance (%)":
                        round(result["compliance"] * 100, 2)
                })

        df = pd.DataFrame(table_rows)
        st.subheader("✅ Compliance Comparison")
        st.dataframe(df, use_container_width=True)

        if st.button("Recommend Best Vendor"):
            with st.spinner("AI generating recommendation..."):
                decision = recommend(evaluations)
                st.subheader("🏆 AI Procurement Recommendation")
                st.write(decision)
