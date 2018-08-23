
"""
Name: Latex Table Generator based on Epidemic Spreading
Author: Pablo Eliseo Reynoso Aguirre
Date: June 5, 2017
Desrcription:

"""

mus = ["mu=0.1", 'mu=0.5', 'm=0.9'];
epidemic_spread_files = ['sf_1000_2_5.txt','erdos_1000_k8.txt','airports_uw'];

latex_tables = [];


latex_table_header = "\n\obegin{quote}\n\obegin{table}[htb]\n\centering\n\obegin{tabular}{S[table-format=1.1]S[table-format=-1.1]S[table-format=-1.1]S[table-format=-1.1]S[table-format=-1.1,table-auto-round=false]}\otoprule";
latex_table_headerf = "\n{$ network\_partition_1 $}   & {$ network\_partition_2 $}  & {$ Jaccard Index $} & {$ 'Normalized Arithmetic Mutual Information' $} & {$ Normalized Variation of Information $}  \o\ \midrule";
latex_table_footer = "\n\end{tabular}\n\caption{Partitions comparissons in network ABCD}\n\label{tab:networks_models}\n\end{table}\n\end{quote}";



for path in networks_paths:
    latex_lines = "";
    i = 1;
    for algorithm in partition_algorithms:
        with open(path+algorithm+file_ext, "r") as f:
            lines = f.readlines()
            latex_line = "\n{$ "+lines[0].split("/")[2].strip()+" $} & "+"{$ "+lines[1].split("/")[3].strip()+"$} & {$ "+lines[13].split(":")[1].strip()+"$} & {$ "+lines[19].split(":")[1].strip()+"$} & {$ "+lines[29].split(":")[1].strip()+"$} \o\ ";
            latex_lines += latex_line;
            #print(latex_line);
        if i == len(partition_algorithms):
            latex_lines += "\obottomrule";
        i+=1;
    latex_tables.append(latex_table_header+latex_table_headerf+latex_lines+latex_table_footer);


print(latex_tables[1]);

latex_file = open("../latex_table_partition_comparissons.txt", "w");
for table in latex_tables:
    latex_file.write(table);
latex_file.close()

