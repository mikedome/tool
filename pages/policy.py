import streamlit as st
import pandas as pd

def show():
    st.title("政策申报")
    
    # 创建不同类型的政策申报卡片
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("科技型中小企业", expanded=True):
            st.write("面向科技创新能力突出的中小企业的扶持政策")
            st.button("申报详情", key="tech_sme")
            
        with st.expander("创新型中小企业", expanded=True):
            st.write("支持具有自主创新能力和发展潜力的中小企业")
            st.button("申报详情", key="innovative_sme")
    
    with col2:
        with st.expander("专精特新中小企业", expanded=True):
            st.write("针对专业化、精细化、特色化、新颖化中小企业的支持政策")
            st.button("申报详情", key="specialized_sme")
            
        with st.expander("高新技术企业", expanded=True):
            st.write("高新技术企业认定及相关优惠政策")
            st.button("申报详情", key="high_tech")

    # 处理按钮点击事件
    if st.session_state.get("specialized_sme", False):
        show_specialized_sme_evaluation()
    elif st.session_state.get("tech_sme", False):
        show_policy_detail("科技型中小企业")
    elif st.session_state.get("innovative_sme", False):
        show_policy_detail("创新型中小企业")
    elif st.session_state.get("high_tech", False):
        show_policy_detail("高新技术企业")

def show_specialized_sme_evaluation():
    st.subheader("专精特新中小企业认定评估")
    
    # 基本条件评估
    st.markdown("### 一、基本认定条件")
    
    market_years = st.number_input("从事特定细分市场年限", min_value=0, value=2, step=1)
    rd_expense = st.number_input("上年度研发费用总额（万元）", min_value=0.0, value=100.0)
    revenue = st.number_input("上年度营业收入总额（万元）", min_value=0.0, value=1000.0)
    rd_ratio = (rd_expense / revenue * 100) if revenue > 0 else 0
    
    # 显示研发费用比例
    st.write(f"研发费用占营业收入比例: {rd_ratio:.2f}%")
    
    # 评分系统
    st.markdown("### 二、评分项目")
    
    # 1. 专业化指标（25分）
    st.markdown("#### 1. 专业化指标（满分25分）")
    
    main_business_ratio = st.selectbox(
        "上年度主营业务收入占营业收入比重",
        ["80%以上", "70%-80%", "60%-70%", "60%以下"]
    )
    
    main_business_growth = st.selectbox(
        "近2年主营业务收入平均增长率",
        ["10%以上", "8%-10%", "6%-8%", "4%-6%", "0%-4%", "0%以下"]
    )
    
    market_score = min(market_years // 2, 5)
    
    product_field = st.selectbox(
        "主导产品所属领域情况",
        [
            "在产业链供应链关键环节及关键领域取得实际成效",
            "属于工业"六基"领域或中华老字号名录",
            "不属于以上情况"
        ]
    )
    
    # 计算专业化得分
    professional_score = calculate_professional_score(
        main_business_ratio, 
        main_business_growth,
        market_score,
        product_field
    )
    
    # 2. 精细化指标（25分）
    st.markdown("#### 2. 精细化指标（满分25分）")
    
    digital_level = st.selectbox(
        "数字化水平",
        ["三级以上", "二级", "一级"]
    )
    
    quality_items = st.multiselect(
        "质量管理水平（可多选）",
        [
            "获得省级以上质量奖荣誉",
            "获得ISO9001等质量管理体系认证",
            "拥有自主品牌",
            "参与制修订标准"
        ]
    )
    
    net_profit_ratio = st.selectbox(
        "上年度净利润率",
        ["10%以上", "8%-10%", "6%-8%", "4%-6%", "2%-4%", "2%以下"]
    )
    
    asset_liability_ratio = st.selectbox(
        "上年度资产负债率",
        ["50%以下", "50%-60%", "60%-70%", "70%以上"]
    )
    
    # 计算精细化得分
    refinement_score = calculate_refinement_score(
        digital_level,
        len(quality_items),
        net_profit_ratio,
        asset_liability_ratio
    )
    
    # 3. 特色化指标（15分）
    st.markdown("#### 3. 特色化指标（满分15分）")
    local_feature_score = st.slider("地方特色指标得分", 0, 15, 0)
    
    # 4. 创新能力指标（35分）
    st.markdown("#### 4. 创新能力指标（满分35分）")
    
    ip_type = st.selectbox(
        "与企业主导产品相关的有效知识产权情况",
        [
            "Ⅰ类高价值知识产权1项以上",
            "自主研发Ⅰ类知识产权1项以上",
            "Ⅰ类知识产权1项以上",
            "Ⅱ类知识产权1项以上",
            "无"
        ]
    )
    
    rd_investment = st.selectbox(
        "上年度研发费用投入",
        [
            "研发费用总额500万元以上或占比10%以上",
            "研发费用总额400-500万元或占比8%-10%",
            "研发费用总额300-400万元或占比6%-8%",
            "研发费用总额200-300万元或占比4%-6%",
            "研发费用总额100-200万元或占比3%-4%",
            "不属于以上情况"
        ]
    )
    
    rd_staff_ratio = st.selectbox(
        "上年度研发人员占比",
        ["20%以上", "10%-20%", "5%-10%", "5%以下"]
    )
    
    rd_institution = st.selectbox(
        "研发机构级别",
        ["国家级", "省级", "市级", "市级以下", "未建立研发机构"]
    )
    
    # 计算创新能力得分
    innovation_score = calculate_innovation_score(
        ip_type,
        rd_investment,
        rd_staff_ratio,
        rd_institution
    )
    
    # 计算总分
    total_score = (professional_score + refinement_score + 
                   local_feature_score + innovation_score)
    
    # 显示评估结果
    st.markdown("### 评估结果")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("专业化得分", f"{professional_score}/25")
    with col2:
        st.metric("精细化得分", f"{refinement_score}/25")
    with col3:
        st.metric("特色化得分", f"{local_feature_score}/15")
    with col4:
        st.metric("创新能力得分", f"{innovation_score}/35")
    with col5:
        st.metric("总分", f"{total_score}/100")
    
    # 判定结果
    basic_conditions_met = (
        market_years >= 2 and
        rd_expense >= 100 and
        rd_ratio >= 3 and
        (revenue >= 1000 or revenue < 1000)  # 这里需要添加融资条件判断
    )
    
    if basic_conditions_met and total_score >= 60:
        st.success("恭喜！您的企业符合专精特新中小企业认定标准！")
    else:
        st.error("抱歉，您的企业暂不符合专精特新中小企业认定标准。")
        
        if not basic_conditions_met:
            st.write("未满足基本条件：")
            if market_years < 2:
                st.write("- 从事特定细分市场时间未达到2年")
            if rd_expense < 100:
                st.write("- 研发费用总额未达到100万元")
            if rd_ratio < 3:
                st.write("- 研发费用占比未达到3%")
            if revenue < 1000:
                st.write("- 营业收入未达到1000万元（如有融资可忽略此项）")
        
        if total_score < 60:
            st.write(f"- 评分未达到60分（当前得分：{total_score}分）")

def calculate_professional_score(main_business_ratio, growth_rate, market_years, product_field):
    score = 0
    
    # 主营业务收入占比得分
    ratio_scores = {
        "80%以上": 5,
        "70%-80%": 3,
        "60%-70%": 1,
        "60%以下": 0
    }
    score += ratio_scores[main_business_ratio]
    
    # 增长率得分
    growth_scores = {
        "10%以上": 10,
        "8%-10%": 8,
        "6%-8%": 6,
        "4%-6%": 4,
        "0%-4%": 2,
        "0%以下": 0
    }
    score += growth_scores[growth_rate]
    
    # 市场年限得分
    score += market_years
    
    # 产品领域得分
    field_scores = {
        "在产业链供应链关键环节及关键领域取得实际成效": 5,
        "属于工业"六基"领域或中华老字号名录": 3,
        "不属于以上情况": 0
    }
    score += field_scores[product_field]
    
    return score

def calculate_refinement_score(digital_level, quality_items_count, profit_ratio, liability_ratio):
    score = 0
    
    # 数字化水平得分
    digital_scores = {
        "三级以上": 5,
        "二级": 3,
        "一级": 0
    }
    score += digital_scores[digital_level]
    
    # 质量管理水平得分
    score += min(quality_items_count * 3, 5)
    
    # 净利润率得分
    profit_scores = {
        "10%以上": 10,
        "8%-10%": 8,
        "6%-8%": 6,
        "4%-6%": 4,
        "2%-4%": 2,
        "2%以下": 0
    }
    score += profit_scores[profit_ratio]
    
    # 资产负债率得分
    liability_scores = {
        "50%以下": 5,
        "50%-60%": 3,
        "60%-70%": 1,
        "70%以上": 0
    }
    score += liability_scores[liability_ratio]
    
    return score

def calculate_innovation_score(ip_type, rd_investment, staff_ratio, institution):
    score = 0
    
    # 知识产权得分
    ip_scores = {
        "Ⅰ类高价值知识产权1项以上": 10,
        "自主研发Ⅰ类知识产权1项以上": 8,
        "Ⅰ类知识产权1项以上": 6,
        "Ⅱ类知识产权1项以上": 2,
        "无": 0
    }
    score += ip_scores[ip_type]
    
    # 研发投入得分
    investment_scores = {
        "研发费用总额500万元以上或占比10%以上": 10,
        "研发费用总额400-500万元或占比8%-10%": 8,
        "研发费用总额300-400万元或占比6%-8%": 6,
        "研发费用总额200-300万元或占比4%-6%": 4,
        "研发费用总额100-200万元或占比3%-4%": 2,
        "不属于以上情况": 0
    }
    score += investment_scores[rd_investment]
    
    # 研发人员占比得分
    staff_scores = {
        "20%以上": 5,
        "10%-20%": 3,
        "5%-10%": 1,
        "5%以下": 0
    }
    score += staff_scores[staff_ratio]
    
    # 研发机构级别得分
    institution_scores = {
        "国家级": 10,
        "省级": 8,
        "市级": 4,
        "市级以下": 2,
        "未建立研发机构": 0
    }
    score += institution_scores[institution]
    
    return score

def show_policy_detail(policy_type):
    st.subheader(f"{policy_type}申报详情")
    
    # 显示申报条件
    st.markdown("### 申报条件")
    if policy_type == "科技型中小企业":
        st.write("""
        1. 在中国境内注册的居民企业
        2. 职工总数不超过500人
        3. 年销售收入不超过2亿元
        4. 资产总额不超过2亿元
        """)
    # ... 其他政策类型的具体条件 ...
    
    # 显示申报材料
    st.markdown("### 所需材料")
    st.write("""
    1. 营业执照
    2. 财务报表
    3. 知识产权证明
    4. 研发项目说明
    """)
    
    # 申报按钮
    st.button("开始申报", key="start_application") 