from beatsperminute import beatsPerMinuteFinal
from gigwise import GigwiseFinal
from fantano import fantanoFinal
from pushData import deployAdditionalReviews
import pandas as pd

# scrape fantano data
fantanoData = fantanoFinal.getFinalReviews()

# scrape Beats Per Minute data
beatsPerMinuteData = beatsPerMinuteFinal.getFinalBeatsPerReviews(5)

# scrape Gigwise data
gigwiseData = GigwiseFinal.getFinalGigwiseReviews()

# post all the reviews
deployAdditionalReviews.postReviews(fantanoData, "The Needle Drop")
deployAdditionalReviews.postReviews(beatsPerMinuteData, "Beats Per Minute")
deployAdditionalReviews.postReviews(gigwiseData, "Gigwise")
