#!/bin/bash

# Download latest .hst files from Abel:
# 
# 	./download_sctc.sh
# 
# Downlaod latest .hst and .vtk files from Abel:
# 
# 	./download_sctc.sh vtk
# 
# Downlaod latest .hst, .topo and .vtk files from Abel:
# 
# 	./download_sctc.sh all
# 
# The folders on Abel downloaded from are listed below.
#
# In order for this script to work, the file ~/.ssh/config must have an entry
# for the alias "abel", e.g.:
#
# 	Host abel
# 		HostName abel.uio.no
# 		IdentityFile ~/.ssh/id_rsa
# 		User sigvaldm
#
# Where "User" is the appropriate username and "IdentityFile" points to the
# correct RSA private key. To ensure this works you should be able to log into
# abel using just "ssh abel" (without necessarily being on the UiO network).
#
# If this does not work, make sure you have a copy of your public key (typically
# named id_rsa.pub) in ~/.ssh on Abel. Make sure all keys has the right
# permission (chmod 600 <key>). Make sure there's a copy of your public key in
# ~/.ssh/authorized_keys on Abel. If not, run:
#
#	cat <public-key> >> ~/.ssh/authorized_keys
#
# Note: If the private key is secured by a passphrase, you will be asked for a
# passphrase when using ssh. That happens many, many times during this script
# and will be ennoying. The risk in turning off the passphrase is that someone
# might steal your computer, or hack into it and steal your private key. But the
# established connection is not less safe without the passphrase. To turn off
# the passphrase:
#	
#	ssh-keygen -p -f <private-key>

for RUN in \
	/usit/abel/u1/sigvaldm/PTetra/Projects/SCTC/Run4_none_35n_0.17eV \
	/usit/abel/u1/sigvaldm/PTetra/Projects/SCTC/Run4_voltages_35n_0.17eV \
	/usit/abel/u1/sigvaldm/PTetra/Projects/SCTC/Run4_guard_35n_0.17eV \
	/usit/abel/u1/sigvaldm/PTetra/Projects/SCTC/Run4_guard-and-voltages_35n_0.17eV \
	/usit/abel/u1/sigvaldm/PTetra/Projects/SCTC/Run4_guard-and-voltages_120n_0.08eV \
    /usit/abel/u1/sigvaldm/PTetra/Projects/SCTC/Run5_largebnd_10n_0.26eV_1.0V \
    /usit/abel/u1/sigvaldm/PTetra/Projects/SCTC/Run5_largebnd_10n_0.26eV_3.0V \
    /usit/abel/u1/sigvaldm/PTetra/Projects/SCTC/Run5_largebnd_10n_0.26eV_5.0V \
    /usit/abel/u1/sigvaldm/PTetra/Projects/SCTC/Run5_largebnd_10n_0.26eV_7.0V \
    /usit/abel/u1/sigvaldm/PTetra/Projects/SCTC/Run5_largebnd_120n_0.08eV_1.0V \
    /usit/abel/u1/sigvaldm/PTetra/Projects/SCTC/Run5_largebnd_120n_0.08eV_3.0V \
    /usit/abel/u1/sigvaldm/PTetra/Projects/SCTC/Run5_largebnd_120n_0.08eV_5.0V \
    /usit/abel/u1/sigvaldm/PTetra/Projects/SCTC/Run5_largebnd_120n_0.08eV_7.0V
do

	HST="$RUN/pictetra.hst" 
	TARGET=${RUN##*/}
	if [ "$1" = "all" ]; then

		echo "Downloading latest .hst, .vtk and .topo files for $TARGET"
		TOP=`ssh abel "ls -t $RUN/pictetra*.topo | head -n 1"`
		VTK=`ssh abel "ls -t $RUN/pictetra*.vtk | head -n 1"`
		SCC=`ssh abel "ls -t $RUN/scc*.vtk | head -n 1"`
		rsync -P abel:$HST abel:$TOP abel:$VTK abel:$SCC $TARGET/

	elif [ "$1" = "vtk" ]; then

		echo "Downloading latest .hst and .vtk files for $TARGET"
		VTK=`ssh abel "ls -t $RUN/pictetra*.vtk | head -n 1"`
		SCC=`ssh abel "ls -t $RUN/scc*.vtk | head -n 1"`
		rsync -P abel:$HST abel:$VTK abel:$SCC $TARGET/

	else
		echo "Downloading latest .hst files for $TARGET"
		rsync -P abel:$HST $TARGET/
	fi
done
