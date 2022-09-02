from re import X
from flask import Flask, render_template
from flask import request
import pickle

app = Flask(__name__)
Filename = 'model.pkl'
file=open(Filename, 'rb')  
model = pickle.load(file)

@app.route('/')
def index_page():
    print(model)
    return render_template('index.html')

@app.route('/predict', methods=['POST', 'GET'])
def predict_logic():
    
    if request.method == 'POST':
        AvailableBankcardCredit = float(request.form.get('AvailableBankcardCredit'))
        EmploymentStatus = float(request.form.get('EmploymentStatus'))
        StatedMonthlyIncome = float(request.form.get('StatedMonthlyIncome'))
        IncomeVerifiable = float(request.form.get('IncomeVerifiable'))
        LoanOriginalAmount = float(request.form.get('LoanOriginalAmount'))
        MonthlyLoanPayment = float(request.form.get('MonthlyLoanPayment'))
        LP_InterestandFees = float(request.form.get('LP_InterestandFees'))
    pred_name = model.predict([[MonthlyLoanPayment,AvailableBankcardCredit,LP_InterestandFees,
        StatedMonthlyIncome,LoanOriginalAmount,EmploymentStatus,IncomeVerifiable]]).tolist()[0]
    x=(StatedMonthlyIncome/LoanOriginalAmount)*100
    yes = "Congrats!! Your loan is a low risk , It should be paid, ROI=",x
    no = "Sorry !! Your loan is a high risk ,It mostly won't be paid, ROI=",x
    result = ''
    if  pred_name == '1':
        result = yes
    else:
        result = no
    return render_template('index.html', pred_name=pred_name, result=result)

if __name__ == "__main__":
    app.run(debug=True)