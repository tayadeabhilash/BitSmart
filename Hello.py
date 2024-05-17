# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Bitsmart",
        page_icon="🚀",
    )

    st.write("# Welcome to BitSmart! 🚀")

    st.sidebar.success("Select the Console above.")

    st.markdown(
        """
        BitSmart is a Machine learing based Bitcoin Price Prediction recommendating 
        Swing trading strategies.

        **👈 Select the console from the sidebar** to see it yourself of what Bitsmart can do!

        ### Team Meambers
        - Umang Patel 
        - Abhilash Tayede
        - Kevin Thomas
        - Ishan Kiran Girgaonkar
      
        ### Disclaimer 
        - The content on this website is for informational purposes only and should not be considered as financial advice. All investment decisions are at your own risk.
        
        ### Educational Purpose
        - The project is implemented for educational purposes during a course work for a class. 
        - It is intended to provide practical experience with Machine Learing methodologies and techniques.
    """
    )


if __name__ == "__main__":
    run()
