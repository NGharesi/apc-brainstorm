Dear Fellow ECoG Researcher,
These are the cue-based hand & tongue movement data described in the Journal of Neuroscience 2007 Manuscript titled: “Spectral Changes in Cortical Surface Potentials during Motor Movement”. The patients only partially overlap with the patients from that study.
Miller, Kai J., Eric C. Leuthardt, Gerwin Schalk, Rajesh PN Rao, Nicholas R. Anderson, Daniel W. Moran, John W. Miller, and Jeffrey G. Ojemann. "Spectral changes in cortical surface potentials during motor movement." Journal of Neuroscience 27, no. 9 (2007): 2424-2432.
Please keep in mind that these anonymized data are from real patients who donated time in a difficult period of their lives to advance our understanding of the brain. Any publication involving these data MUST include the following in the methods section of the manuscript, without modification: 
Ethics statement: All patients participated in a purely voluntary manner, after providing informed written consent, under experimental protocols approved by the Institutional Review Board of the University of Washington (#12193). All patient data was anonymized according to IRB protocol, in accordance with HIPAA mandate. It was made available through the library described in “A Library of Human Electrocorticographic Data and Analyses” by Kai Miller [Reference], freely available at https://searchworks.stanford.edu/view/zk881ps0522. All patient data was anonymized according to IRB protocol, in accordance with HIPAA mandate. These data originally appeared in the manuscript “Spectral Changes in Cortical Surface Potentials during Motor Movement” published in Journal of Neuroscience in 2007 [Reference].

 “Cue-based movement task”: Patients performed simple, repetitive, motor tasks of hand (synchronous flexion and extension of all fingers, i.e., clenching and releasing a fist at a self-paced rate of ~1-2 Hz) or tongue (opening of mouth with protrusion and retraction of the tongue, i.e., sticking the tongue in and out, also at ~1-2 Hz). These movements were performed in an interval-based manner, alternating between movement and rest, and the side of move- ment was always contralateral to the side of cortical grid placement. 
There were between 30 and 75 cue presentations for each movement modality. Cues for motor movement were delivered visually in a 10 x 10 cm presentation window at a distance of 75–100 cm from patient. Visual cues were presented using the BCI 2000 program with a written word indicating the specific body part to be moved (typically, multiple movement types were interleaved in each experimental run). Stimuli were presented for 2 s or 3 s cue blocks, followed by rest intervals (indicated by a blank screen) of the same length. The patients were instructed to perform repetitive, self-paced motor movement, alternating with rest intervals of the same length (indicated by the absence of the cuing target). Repetitive motion, rather than tonic contraction, was intended to accentuate the spectral shift during each interval.
The basic datafiles (in MATLAB format) are named “##_mot_t_h.mat” in the folder data/##, where ## denotes the 2 letter patient code. This code is not the patient’s initials. 

Each datafile has 2 variables:

"stim" (time x 1): This is what was stimulus was on the screen at each point in time. 
0: blank screen
11: tongue movement
12: hand movement

"data" (time x number of channels): These are the data. I have attempted to remove the contaminated channels. Data were recorded with respect to a scalp reference.
sampled at 1000Hz
scale factor: 1 amplifier unit = .0298 microvolts
built-in band pass 0.15 to 200 Hz, 
- but a 1 pole band pass, so there is no sharp corner at 200Hz. 
-The amplitude roll-off function is in the file “ns_1k_1_300_filt.mat”
For all patients, there is a file titled “##_electrodes.mat” in the folder electrodes/##,
Each file contains a single variable:
"electrodes" (number of channels x 3): Electrode locations, in Taliarach coordinates, for plotting on the standardized brain. These were obtained using the LOC package, and can be plotted with it as well (code in “loc” folder). From “Cortical electrode localization from X-rays and simple mapping for electrocorticographic research: The “Location on Cortex” (LOC) package for MATLAB” in J Neurosci Meth, 2007.

For several patients, there is a file titled “##_brains.mat” in the folder brains/##,
Each file contains two variables:
"brain": This is a structure representing the tessellated brain surface. It can easily be plotted with the CTMR package (see “Automated electrocorticographic electrode localization on individually rendered brain surfaces” by D Hermes, et al in Journal of Neuroscience Methods, 2009)
"locs" (number of channels x 3): Electrode locations, for plotting on the rendered brain.


In order to reproduce the analyses from the manuscript, open and examine the file “mot_th_master. m”. Each step of analysis is shown clearly in the functions called from this file. Intermediate processed data are saved automatically in the analysis folder, and figures are generated and saved to the figs folder. Please note that I use a “code-section” approach to programming (each section headed by “%%”), and it is intended that you evaluate each section (control-enter or command-enter) in sequence to understand each step.

Please note that the behavior may not have aligned as well to the cues as we might hope. These code scripts are not the original from the manuscript and were written in 2015 to mimic that analysis. Some of these datafiles also appear in the imagery dataset, where finger position was retained.

Note that the folders “loc” and “toolbox” from the root directory (zip files of the ECoG library) must be included in your MATLAB path for the analyses to work properly.

Note that electrode montages may be different from same task in same patient elsewhere in this library (when electrodes were artifactual for a different task within the same experiment, those electrodes would be deleted across to the board, to ensure consistent montage across all tasks for the experiment).

Best Wishes!
Kai Miller,
Stanford University, 2015 (revised 2018)
kai.miller@stanford.edu, miller.kai@mayo.edu
