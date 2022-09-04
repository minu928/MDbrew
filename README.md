# MDpy

MDpy is a tool for postprocessing of LAMMPS data or lammpstrj

MDpy
  -> Opener
      => DumpOpener : for dump file (ex. dump.lammpstrj)
      => DataOpener : for data file (ex. data.lammps)
  -> tools
      => do_progress_bar : make a local progress bar with iteration
      => timeCount : decorator for get execute time
      => LinearRegression : Class for linear regression
  -> MSD
      => Class for get MSD data with position data [ lagtime, Number of Particle, pos ]
  -> RDF
      => Class for get RDF data with position data [ lagtime, Number of Particle, pos ]
