<h2>qe-lab: A Quantum ESPRESSO post-processing tool</h2>

<b>What can it currently do?</b>
<ul style="list-style-type:disc;">
	<li>Find Total energy and Fermi level given an SCF output file</li>
	<li>Determine band gap for semiconductors given a well-sampled GNU-Format bands.x output file</li>
</ul>
<b>What to do next?</b>
<ul style="list-style-type:disc;">
	<li>Function to produces band structure from GNU-Format bands.x using matplotlib</li>
	<li>Functino to produce density of states from data file</li>
</ul>
<b>What to do in the future?</b>
<ul style="list-style-type:disc;">
	<li>database capabilities</li>
	<li>calculation seeker</li>
	<li>user interface</li>
</ul>

</ul>
<b>Requirements</b>
<ul style="list-style-type:disc;">
	<li>Python (matplotlib, numpy)</li>
	<li>UNIX like CLI</li>
</ul>
<b>Assumptions</b>
<ul style="list-style-type:disc;">
	<li>You are in the pw.x scf folder</li>
	<li>With reference to current directory, "bands.gnu" is located in "./bands/"</li>
	<li>SCF log file is named as "INPUT"</li>
</ul>

<b>How to run</b>
<ol>
	<li>Go to the pw.x SCF folder</li>
	<li>run as "python [qelab.py DIRECTORY]/qelab.py"</li>
</ol>
