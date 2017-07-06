# Static methods that 


def fillTable(self, string):
    """Build a sorted table of all non-pronoun tags along with their 
    start and stop indices. 
    """
    
    keywordTable = KeywordInstanceTable()
    string = self.get("1.0", tk.END)
    
    # Ideally, make a generator for each relevant line
    iterator = re.finditer("\w+", string) 
    keyword = ""
    cacheItem = KeywordInstance()
    foundMatch = False
    word = next(iterator)
    
    try:
        while True: # Gods of CS, forgive this infinite loop.
            inx = int(self.index("1.0+%sc" % word.start()).split(".")[0])
            
            # Only run the next bit if it's an interviewee.
            if  (inx % 4 - 1) != 0:
                testCode = self.indexObject.multiTest(word.group().lower())

                # For this next block of if, elif, else:
                # Using the testCode, save object information:
                # 2 = unique match found, 
                # 1 = potential match,
                # 0 = no match.                     
                if testCode == 0:
                    
                    # This is the point when an entry is actually 
                    # saved. When it finds a match, it waits until 
                    # it hits a zero to save it, in case there are a
                    # couple keys like so: "фон", "фон триер". We  
                    # want the second, longer tag, not the shorter.
                    if foundMatch:
                        cacheItem["string"] = keyword
                        keywordTable.append(cacheItem)  
                        
                        # Reset the saved values.
                        keyword = ""
                        cacheItem = KeywordInstance()
                        foundMatch = False
                        
                        # Continue rechecks the same word with a re-
                        # set multiTest, in case two keywords are 
                        # next to each other.
                        continue

                    keyword = ""
                    cacheItem = KeywordInstance()
                
                elif testCode == 1:
                    # If there is a word, add a space before the
                    # next one.                       
                    if keyword != "":
                        keyword += " "
                    else:
                        cacheItem["start"] = word.start()
                    keyword += word.group()
                    
                else:
                    if keyword != "":
                        keyword += " "
                    else:
                        cacheItem["start"] = word.start()
    
                    keyword += word.group()
                    cacheItem["stop"] = word.end()
                    foundMatch = True
                    
            word = next(iterator)

    except StopIteration:
        # May need to save the last information, in case the final 
        # word is a keyword
        pass

    return keywordTable

