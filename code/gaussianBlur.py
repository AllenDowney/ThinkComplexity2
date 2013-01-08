"""PHILIPZLOH"""

def gaussianBlur(arrayIn, levels):
    import numpy
    
    R, C = numpy.shape(arrayIn)
    arrayOut = numpy.array(arrayIn, copy=True)
    
    for l in range(levels):
        for r in range(R):
            for c in range(C):
                new = 0.8 * arrayIn[r,c]
                failed = 0
                try: new += 0.2 * arrayIn[r-1,c]
                except IndexError: failed += 0.2
                try: new += 0.2 * arrayIn[r+1,c]
                except IndexError: failed += 0.2
                try: new += 0.2 * arrayIn[r,c-1]
                except IndexError: failed += 0.2
                try: new += 0.2 * arrayIn[r,c+1]
                except IndexError: failed += 0.2
                try: new += 0.05 * arrayIn[r-1,c-1]
                except IndexError: failed += 0.05
                try: new += 0.05 * arrayIn[r+1,c-1]
                except IndexError: failed += 0.05
                try: new += 0.05 * arrayIn[r-1,c+1]
                except IndexError: failed += 0.05
                try: new += 0.05 * arrayIn[r+1,c+1]
                except IndexError: failed += 0.05
                arrayOut[r,c] = new + failed * arrayIn[r,c]
        
        arrayOut /= arrayOut.max()
        arrayIn[:] = arrayOut[:]
    
    return arrayOut