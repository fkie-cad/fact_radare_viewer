# Radare Viewer

Host several radare instances and forward their Web-UIs to a single outgoing port.
New instances can be triggered from outside by REST requests, containing a binary for analysis.
Response then contains the link to the Web-UI as seen from outside.

Configurations are necessary for target port and host ip address.

:exclamation: This only works with recent version of r2 webUI. Normal r2 installation has to be patched to make javascript work.

### Copyright Fraunhofer FKIE 2018
