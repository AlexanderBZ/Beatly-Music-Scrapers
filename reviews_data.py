from beatsperminute import beatsPerMinuteFinal
from gigwise import GigwiseFinal
from fantano import fantanoFinal
from vinylChapters import vinylChaptersFinal
from pushData import deployAdditionalReviews
import pandas as pd

# scrape fantano data
fantanoData = fantanoFinal.getFinalReviews()

# scrape Beats Per Minute data
beatsPerMinuteData = beatsPerMinuteFinal.getFinalBeatsPerReviews(10)

# scrape Gigwise data
gigwiseData = GigwiseFinal.getFinalGigwiseReviews()

# scrape Gigwise data
vinylChaptersData = vinylChaptersFinal.getFinalVinylChaptersReviews(10)

# post all the reviews
deployAdditionalReviews.postReviews(fantanoData, "The Needle Drop")
deployAdditionalReviews.postReviews(beatsPerMinuteData, "Beats Per Minute")
deployAdditionalReviews.postReviews(gigwiseData, "Gigwise")
deployAdditionalReviews.postReviews(vinylChaptersData, "Vinyl Chapters")