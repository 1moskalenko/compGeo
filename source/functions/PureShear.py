import numpy as np
import matplotlib.pyplot as plt

def PureShear(pts,st1,ninc):
	'''
	PureShear computes and plots displacement paths and
	progressive finite strain history for pure shear with
	maximum stretching parallel to the X1 axis
	
	USE: paths,pfs = PureShear(pts,st1,ninc)
	
	pts: npoints x 2 matrix with X1 and X3 coord. of points
	st1 = Maximum principal stretch
	ninc = number of strain increments
	paths = displacement paths of points
	pfs = progressive finite strain history. column 1 =
		orientation of maximum stretch with respect to X1
		in degrees, column 2 = maximum stretch magnitude
	NOTE: Intermediate principal stretch is 1.0 (Plane 
		strain). Output orientations are in radians
	
	Python function based on the Matlab function
	PureShear in Allmendinger et al. (2012)
	'''
	# Compute minimum principal stretch and incr. stretches
	st1inc=st1**(1.0/ninc)
	st3=1.0/st1
	st3inc=st3**(1.0/ninc)

	# Initialize displacement paths
	npts = np.size(pts,0) # Number of points
	paths = np.zeros((ninc+1,npts,2))
	paths[0,:,:] = pts # Initial points of paths

	# Calculate incremental deformation gradient tensor
	F = np.array([[st1inc, 0.0], [0.0, st3inc]])
	
	# Initialize figure
	fig = plt.figure(figsize=(15,5)) # Define the size
	ax1 = fig.add_subplot(1, 2, 1)
	ax2 = fig.add_subplot(1, 2, 2)

	# Compute displacement paths
	for i in range(npts): # for all points
		for j in range(ninc+1): # for all strain increments
			for k in range(2):
				for L in range(2):
					paths[j,i,k] = F[k,L]*paths[j-1,i,L] + paths[j,i,k]
		# Plot displacement path of point
		xx = paths[:,i,0]
		yy = paths[:,i,1]
		ax1.plot(xx,yy,'k.-')

	# Plot initial and final polygons
	inpol = np.zeros((npts+1,2))
	inpol[0:npts,]=paths[0,0:npts,:]
	inpol[npts,] = inpol[0,]
	ax1.plot(inpol[:,0],inpol[:,1],'b-')
	finpol = np.zeros((npts+1,2))
	finpol[0:npts,]=paths[ninc,0:npts,:]
	finpol[npts,] = finpol[0,]
	ax1.plot(finpol[:,0],finpol[:,1],'r-')
	
	# Release plot and set axes
	ax1.set_xlabel('X1')
	ax1.set_ylabel('X3')
	ax1.grid()
	ax1.axis('equal')
	
	# Initalize progressive finite strain history
	pfs = np.zeros((ninc+1,2))
	pfs[0,:] = [0, 1] #Initial state

	# Calculate progressive finite strain history
	for i in range(1,ninc+1):
		# Determine the finite deformation gradient tensor
		finF = np.linalg.matrix_power(F, i)
		# Determine Green deformation tensor
		G = np.dot(finF,finF.conj().transpose())
		# Stretch magnitude and orientation: Maximum 
		# eigenvalue and their corresponding eigenvectors
		# of Green deformation tensor
		D, V = np.linalg.eigh(G)
		pfs[i,0] = np.arctan(V[1,1]/V[0,1])
		pfs[i,1] = np.sqrt(D[1])

	# Plot progressive finite strain history
	ax2.plot(pfs[:,0]*180/np.pi,pfs[:,1],'k.-')
	ax2.set_xlabel('Θ deg')
	ax2.set_ylabel('Maximum finite stretch')
	ax2.set_xlim(-90,90)
	ax2.set_ylim(1,max(pfs[:,1])+0.5)
	ax2.grid()
	
	# show plot
	plt.show()

	return paths,pfs