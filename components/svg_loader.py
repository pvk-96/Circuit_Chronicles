import streamlit as st

def show_svg_loader(text="Loading data..."):
    loader_html = f"""
    <div class="svg-loader-wrapper">
        <div class="svg-loader">
            <svg
                class="logo"
                xmlns="http://www.w3.org/2000/svg"
                width="150"
                height="150"
                viewBox="0 0 225 225"
                preserveAspectRatio="xMidYMid meet"
            >
                <g transform="translate(0,225) scale(0.1,-0.1)">
                    <!-- PATH DATA -->
                    <path d="M112 1368 c-32 -32 13 -161 58 -166 l25 -3 -25 13 c-32 17 -53 62
                    -54 113 l-1 40 65 -3 c69 -3 345 -29 402 -37 l33 -5 -29 10
                    ... (TRUNCATED FOR READABILITY) ...
                    </path>
                </g>
            </svg>
        </div>
        <p class="svg-loader-text">{text}</p>
    </div>
    """

    placeholder = st.empty()
    placeholder.markdown(loader_html, unsafe_allow_html=True)
    return placeholder
