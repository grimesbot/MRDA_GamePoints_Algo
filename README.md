Info about the WFTDA rankings algorithm can be found on their website. I've implimented the same type of algorithm here. 
For information about the math involved, please go to that source.
https://static.wftda.com/files/competition/2023-WFTDA-Rankings-Algorithm.pdf

Quick summary:
Each team has a GPA - Game Points Average. This can be used as a direct comparison to the strength of another team. For 
example, a team with a GPA of 600 should outscore a team with a GPA of 300 by a 2:1 ratio. I think this makes intuitive 
"gut checks" pretty easy when looking at the algo results.

Only games from the previous 12 months count. And games that are more than 6 months old have less weight. This can be 
adjusted. WFTDA sets those older games to 0.5 weight. I currently have them set to 0.25 weight, which seems to be more 
in line with MRDA membership, who want to see more recent scores influence team rankings more heavily.
