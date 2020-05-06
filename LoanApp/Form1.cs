using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace LoanApp
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            this.gradeComboBox.Items.AddRange(new string[] { "A", "B", "C", "D", "E", "F", "G" });
            this.gradeComboBox.SelectedIndex = 0;
            this.homwOwnerComboBox.Items.AddRange(new string[] { "MORTGAGE", "RENT", "OWN" });
            this.homwOwnerComboBox.SelectedIndex = 0;
            this.purposeComboBox.Items.AddRange(new string[] { "debt_consolidation", "credit_card", "major_purchase",
                                                                "home_improvement", "moving", "small_business",
                                                                "medical", "car", "vacation", "house", "renewable_energy", "other" });
            this.purposeComboBox.SelectedIndex = 9;
            this.employedDomainUpDown.Items.AddRange(new string[] { "less < 1", "1", "2",
                                                                    "3", "4", "5",
                                                                    "6", "7", "8", "9", "10+" });
            this.employedDomainUpDown.SelectedIndex = 0;
        }

        private void creditButton_Click(object sender, EventArgs e)
        {
            this.statusTextBox.Text = "";
            int loan_amount = int.Parse(this.loanAmountTextBox.Text);
            double int_rate = Convert.ToDouble(this.intRateTextBox.Text);
            double installment = Convert.ToDouble(this.installmentTextBox.Text);
            string grade = this.gradeComboBox.SelectedItem.ToString();
            int employed = this.employedDomainUpDown.SelectedIndex;
            string owner = this.homwOwnerComboBox.SelectedItem.ToString();
            int income = int.Parse(this.annualTextBox.Text);
            string purpose = this.purposeComboBox.SelectedItem.ToString();
            int credit_inq = int.Parse(this.inqTextBox.Text);
            int incidents = int.Parse(this.pastTextBox.Text);


            var module_folder = @"D:\Workspace\VisualStudioProj\WindowsToPythonAI\python_model";
            var module_name = "run_keras_model";
            var class_name = "LoanModel";
            var def_name = "predict_this";

            //Model input arguments preparation
            var methodArguments = new PythonCallerArgs();

            methodArguments.AddArg("loan_amnt", loan_amount);
            methodArguments.AddArg("int_rate", int_rate);
            methodArguments.AddArg("installment", installment);
            methodArguments.AddArg("grade", grade);
            methodArguments.AddArg("emp_length", employed);
            methodArguments.AddArg("home_ownership", owner);
            methodArguments.AddArg("annual_inc", income);
            methodArguments.AddArg("purpose", purpose);
            methodArguments.AddArg("inq_last_12m", credit_inq);
            methodArguments.AddArg("delinq_2yrs", incidents);

            methodArguments.AddMetaArg("caller", "WindowsToPythonAI");

            // Now we can create a caller object and bind it to the model
            var pyCaller = new PythonCaller(module_folder, module_name);
            Dictionary<string, string> resultJson = pyCaller.CallClassMethod(class_name, def_name, methodArguments);
            this.statusTextBox.Text = resultJson["prediction"];
        }
    }
}
