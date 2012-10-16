all: SimplePoissonNG Tests

SimplePoissonNG: SimplePoissonNG2D SimplePoissonNG3D

SimplePoissonNG2D: MEF90 chkpaths
	make -C objs/${PETSC_ARCH} -f ../../SimplePoissonNG/makefile MEF90_DIM=2 

SimplePoissonNG3D: MEF90 chkpaths
	make -C objs/${PETSC_ARCH} -f ../../SimplePoissonNG/makefile MEF90_DIM=3 

MEF90: chkpaths
	make -C objs/${PETSC_ARCH} -f ../../MEF90/makefile

chkpaths: objs/${PETSC_ARCH} bin/${PETSC_ARCH}

objs/${PETSC_ARCH}:
	@mkdir -p objs/${PETSC_ARCH}
bin/${PETSC_ARCH}:
	@mkdir -p bin/${PETSC_ARCH}

clean:
	rm -Rf objs/${PETSC_ARCH}
	rm -Rf bin/${PETSC_ARCH}
