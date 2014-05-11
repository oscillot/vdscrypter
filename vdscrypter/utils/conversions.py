def get_microspf_from_fps(fps):
    spf = 1/float(fps)
    mspf = spf * 1000
    microspf = mspf * 1000
    return microspf