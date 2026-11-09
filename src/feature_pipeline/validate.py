import json
import os
os.environ.setdefault("GX_ANALYTICS_ENABLED", "false")
import great_expectations as gx
from src.feature_pipeline.preprocess import CUSTOMER_COLUMNS, DOMAINS


def validate_data(df,report_path,cleaned=False):
    required = CUSTOMER_COLUMNS + ["Churn"]
    missing = sorted(set(required)- set(df.columns))
    if missing:
        report = {"success": False, "missing_columns":missing}

    else:
        context = gx.get_context(mode="ephemeral")
        source = context.data_sources.add_pandas("churn")
        asset = source.add_dataframe_asset("customers")
        batch_definition = asset.add_batch_definition_whole_dataframe("all_rows")
        suite = context.suites.add(gx.ExpectationSuite(name="cleaned" if cleaned else "incoming"))
        rules = [gx.expectations.ExpectTableRowCountToBeBetween(min_value=1),
                 gx.expectations.ExpectColumnValuesToBeUnique(column="customerID")]
        # Blank TotalCharges is an allowed incoming issue, but must be resolved after cleaning.
        for column in required:
            if cleaned or column != "TotalCharges":
                rules.append(gx.expectations.ExpectColumnValuesToNotBeNull(column=column))
        for column in ["tenure", "MonthlyCharges"] + (["TotalCharges"] if cleaned else []):
            rules.append(gx.expectations.ExpectColumnValuesToBeBetween(column=column, min_value=0))
        for column, values in DOMAINS.items():
            rules.append(gx.expectations.ExpectColumnValuesToBeInSet(column=column, value_set=values))
        labels = [0, 1] if cleaned else ["Yes", "No", 0, 1]
        rules.append(gx.expectations.ExpectColumnValuesToBeInSet(column="Churn", value_set=labels))
        for rule in rules:
            suite.add_expectation(rule)
        definition = context.validation_definitions.add(gx.ValidationDefinition(
            name="check_customers", data=batch_definition, suite=suite))
        result = definition.run(batch_parameters={"dataframe": df}, result_format="BOOLEAN_ONLY")
        report = result.to_json_dict()
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    if not report["success"]:
        raise ValueError(f"Data validation failed. Read {report_path}")
    return report
