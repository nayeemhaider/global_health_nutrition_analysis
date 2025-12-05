import streamlit as st
import pandas as pd
import plotly.express as px

from queries import (
    get_year_range,
    get_countries,
    get_global_overview,
    get_top_life_expectancy,
    get_doctors_vs_mortality,
    get_diet_vs_cvd,
    get_gender_gap_year,
    get_country_story,
)

st.set_page_config(
    page_title="Global Health & Nutrition Analysis Dashboard",
    layout="wide"
)

st.title("Global Health & Nutrition Analysis Dashboard")

# Sidebar controls
years = get_year_range()
default_year = max(years) if years else None

st.sidebar.header("Filters")
selected_year = st.sidebar.selectbox("Year", options=years, index=len(years) - 1 if years else 0)
selected_country = st.sidebar.selectbox("Country (for story view)", options=["All"] + get_countries())
st.sidebar.markdown("---")
st.sidebar.write("Use the tabs below to explore different parts of the story.")

tab_overview, tab_access, tab_diet, tab_gender, tab_country = st.tabs(
    ["Global Overview", "Access & Mortality", "Diet & Cardiovascular", "Gender & Inequality", "Country Story"]
)

with tab_overview:
    st.subheader("Global Life Expectancy and Child Mortality")

    df = get_global_overview(selected_year)
    if df.empty:
        st.warning("No data for the selected year.")
    else:
        col1, col2, col3 = st.columns(3)

        global_le = df["life_expectancy"].mean()
        global_imr = df["infant_mortality_rate"].mean()
        global_u5 = df["under5_mortality_rate"].mean()

        col1.metric("Global average life expectancy", f"{global_le:.1f} years")
        col2.metric("Global infant mortality", f"{global_imr:.1f} per 1,000")
        col3.metric("Global under-5 mortality", f"{global_u5:.1f} per 1,000")

        st.markdown("### Life expectancy distribution")
        fig_hist = px.histogram(df, x="life_expectancy", nbins=30)
        st.plotly_chart(fig_hist, use_container_width=True)

        st.markdown("### Top 10 countries by life expectancy")
        top_df = get_top_life_expectancy(selected_year)
        fig_bar = px.bar(top_df, x="country", y="life_expectancy")
        st.plotly_chart(fig_bar, use_container_width=True)

with tab_access:
    st.subheader("Healthcare Access and Child Mortality")

    df_access = get_doctors_vs_mortality(selected_year)
    if df_access.empty:
        st.warning("No data for the selected year range.")
    else:
        st.markdown("Scatter plot of doctors per 1,000 people vs infant mortality (5-year average).")
        fig_scatter = px.scatter(
            df_access,
            x="doctors_avg",
            y="imr_avg",
            hover_name="country",
            labels={
                "doctors_avg": "Doctors per 1,000 (avg last 5 years)",
                "imr_avg": "Infant mortality rate (avg last 5 years)"
            }
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

        st.markdown("Table of countries sorted by infant mortality:")
        st.dataframe(df_access.sort_values("imr_avg"))

with tab_diet:
    st.subheader("Diet and Cardiovascular Deaths")

    df_diet = get_diet_vs_cvd(selected_year)
    if df_diet.empty:
        st.warning("No diet and cardiovascular data for the selected year.")
    else:
        st.markdown("Scatter: animal protein calories vs share of deaths from cardiovascular diseases.")
        fig_scatter_diet = px.scatter(
            df_diet,
            x="animal_kcal",
            y="pct_death_cardiovascular",
            hover_name="country",
            size="total_fruit_consumption",
            labels={
                "animal_kcal": "Daily calories from animal protein",
                "pct_death_cardiovascular": "% of deaths due to cardiovascular causes",
                "total_fruit_consumption": "Fruit consumption (proxy, various fruits)"
            }
        )
        st.plotly_chart(fig_scatter_diet, use_container_width=True)

        st.markdown("Distribution of diet calories")
        fig_box = px.box(
            df_diet,
            y=["animal_kcal", "plant_kcal", "fat_kcal", "carb_kcal"],
            points="all"
        )
        st.plotly_chart(fig_box, use_container_width=True)

with tab_gender:
    st.subheader("Gender Gaps in Life Expectancy")

    df_gender = get_gender_gap_year(selected_year)
    if df_gender.empty:
        st.warning("No gender data for the selected year.")
    else:
        st.markdown("Female vs male life expectancy by country.")
        df_long = df_gender.melt(
            id_vars="country",
            value_vars=["le_female", "le_male"],
            var_name="gender",
            value_name="life_expectancy"
        )
        df_long["gender"] = df_long["gender"].map({"le_female": "Female", "le_male": "Male"})

        fig_dumbbell = px.scatter(
            df_long,
            x="life_expectancy",
            y="country",
            color="gender",
            hover_name="country"
        )
        st.plotly_chart(fig_dumbbell, use_container_width=True)

        st.markdown("Top countries by female–male life expectancy gap.")
        st.dataframe(
            df_gender.sort_values("le_gap_female_minus_male", ascending=False).head(20)
        )

with tab_country:
    st.subheader("Country Story")

    if selected_country == "All":
        st.info("Select a specific country in the sidebar to see its story.")
    else:
        df_story = get_country_story(selected_country)
        if df_story.empty:
            st.warning("No data for this country.")
        else:
            col1, col2 = st.columns(2)
            col1.markdown(f"### {selected_country}")
            col1.write(
                f"Data from {df_story['year'].min()} to {df_story['year'].max()}."
            )

            # life expectancy and under-5 mortality
            fig_le = px.line(df_story, x="year", y="life_expectancy", title="Life expectancy over time")
            fig_u5 = px.line(df_story, x="year", y="under5_mortality_rate", title="Under-5 mortality over time")

            col1.plotly_chart(fig_le, use_container_width=True)
            col2.plotly_chart(fig_u5, use_container_width=True)

            st.markdown("### Access and diet indicators over time")
            indicators = ["uhc_coverage", "doctors", "basic_water", "basic_sanitation_total"]
            fig_access = px.line(
                df_story,
                x="year",
                y=indicators,
                labels={"value": "Value", "variable": "Indicator"},
            )
            st.plotly_chart(fig_access, use_container_width=True)

            diet_cols = ["animal_kcal", "plant_kcal", "fat_kcal", "carb_kcal"]
            available_diet_cols = [c for c in diet_cols if c in df_story.columns and df_story[c].notna().any()]
            if available_diet_cols:
                fig_diet = px.line(
                    df_story,
                    x="year",
                    y=available_diet_cols,
                    labels={"value": "Calories", "variable": "Diet component"}
                )
                st.plotly_chart(fig_diet, use_container_width=True)

            # Simple auto-summary
            start_year = int(df_story["year"].min())
            end_year = int(df_story["year"].max())
            le_start = df_story.loc[df_story["year"] == start_year, "life_expectancy"].mean()
            le_end = df_story.loc[df_story["year"] == end_year, "life_expectancy"].mean()
            le_change = le_end - le_start

            st.markdown("### Summary")
            st.write(
                f"Between {start_year} and {end_year}, life expectancy in {selected_country} "
                f"changed by approximately {le_change:.1f} years. "
                "The charts above show how this change relates to child mortality, "
                "healthcare access and diet patterns."
            )
