import streamlit as st
from pydantic import BaseModel, ValidationError
import json
from pprint import pprint

st.set_page_config(layout="wide", page_title="CIBI - Can I Buy It?")

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(
            rgba(0, 0, 0, 0.85)
        ),
        url("https://images.unsplash.com/photo-1542906484-f6a89f408345?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-size: cover;
        background-position: center;
    }
    /* Hide Streamlit header & hamburger */
    header[data-testid="stHeader"] {
        display: none;
    }

    /* Hide the top padding that remains */
    div.block-container {
        padding-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

class Home(BaseModel):
    price: int
    interest_rate: float
    min_amortization: float
    down_payment: int
    monthly_fee: int
    address: str

# Function for loading homes from json into a list of Home objects
def load_homes():
    file_path = "homes.json"
    print(file_path)
    home_list = []
    
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for item in data:
        try:
            home = Home(**item)
            home_list.append(home)
        except ValidationError as e: 
            print(f"Validation error: {e}")
            
    return home_list    

# Function for showing a home in the left column (streamlit module style)
def show_home_in_list(home):
    with st.expander(label=f"{home.address} - {home.price} SEK"):
        st.text(f"Down payment: {home.down_payment} SEK")
        st.text(f"Monthly fee: {home.monthly_fee} SEK")

# Streamlit app/UI  
def streamlit_app():    
    home_list = load_homes()
    home_list_sorted = home_list # To fix
    
    st.header("Can I Buy It?")
    
    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        
        # Available homes column
        with col1:
            with st.container(border=True):
                st.subheader("Available Homes")
                for home in home_list:
                    show_home_in_list(home)
            
        # User input column
        with col2:
            with st.container(border=True):
                st.subheader("Calculate")
                income = st.number_input(label="Yearly Income (before taxes)", step=10000)  # Inkomst
                assets = st.number_input(label="Liquid Assets", step=10000)  # Tillgångar
                
                selected_home = st.selectbox(
                    label="Select the home you are interested in",
                    index=None,
                    options=home_list_sorted,
                    format_func=lambda h: f"{h.address} - {h.price} SEK",
                    key="selected_home"
                )
                
                pprint(selected_home)  # Now this prints a Home object, not a string!

                # Button for doing the calculations
                if st.button(type="primary", label="Calculate", use_container_width=True):
                    final_answer = calculate_answer(income, assets, selected_home)
                    with st.container(border=True): 
                        st.subheader("Your answer")
                        st.text(final_answer)
                else:
                    with st.container():
                        st.text("Fill out your details and click on 'Calculate' to get an answer.")
        
        # Home Details (?)
        with col3:
            with st.container(border=True):
                st.subheader("Home Details")
                if not selected_home:
                    st.text("Select the home you want to buy to show the details.")
                else:
                    st.markdown(f"**{selected_home.address}**")
                    st.write(f"Price: {selected_home.price} SEK")
                    st.write(f"Interest rate: {selected_home.interest_rate * 100:.1f}% - {selected_home.price * selected_home.interest_rate / 12:.0f} SEK")
                    st.write(f"Amortization: {selected_home.min_amortization * 100:.0f}% - {selected_home.price * selected_home.min_amortization / 12:.0f} SEK")
                    st.write(f"Down payment: {selected_home.down_payment} SEK")
                    st.write(f"Montly fee: {selected_home.monthly_fee} SEK/month")


# Funktioner för uträkning
def has_down_payment(assets : int, down_payment):
    if assets >= down_payment:
        print("User can pay")
        return True
    else:
        print("User can't pay")
        return False

def calculate_answer(income: int, assets: int, home) -> str:
    print("Entering function")
    highest_loan = income * 5
    
    #home values
    total_price = home.price
    down_payment = home.down_payment
    min_amort = home.min_amortization
    interest_rate = home.interest_rate
    monthly_fee = home.monthly_fee
    
    print("Checking if user can pay")
    can_pay_down_payment = has_down_payment(assets, down_payment)
    loan = total_price - down_payment
    
    interest_cost = loan * interest_rate / 12
    amort_cost = loan * min_amort / 12    
    monthly_cost = interest_cost + amort_cost + monthly_fee
    
    answer = "Unfortunatley you cannot afford this home."
    
    if not can_pay_down_payment:
        answer += " You do not have enough assets for the down payment."
        return answer
    else:
        if total_price > highest_loan:
            answer += " Your yearly income is not high enough."
            return answer
        else:
            if monthly_cost > income * 0.35:
                print("5")
                answer = f"Unfortunatley you cannot afford this home. This monthly cost will be {monthly_cost} sek"
                return answer
            else:
                print("6")
                answer = "Congratulations you can afford this home!"
                return answer
            
streamlit_app()
            
