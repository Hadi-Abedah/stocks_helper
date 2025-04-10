<h1> This repository is meant to help me streamline my stock investment practices. </h1> 
<ul>
  <li><b>alerts</b> package would use logic defined in other packages and send the results as a message using CallMeBot API.</li>
  <li><b>google_docs</b> package will write the expected date for the next earning announcements for the tickers listed in companies.csv, in a Google Docs file. </li>
  <li><b>news</b> is a package that will take care of informing me of any breaking news regarding stocks in my portfolio(the code needs major refactoring currently) </li>
  <li><b>perecntage_change</b> package read from a list of stocks and their description available as a CSV file to get percentage changes during certain periods </li>
  <li><b>snaptrade</b> package will utilize snaptrade API to access my stoke broker APP and pull data related to my actual holding, transactions and available cash, it will write transactions to a Google Sheets file using double-entry accounting principles  </li>
</ul>
