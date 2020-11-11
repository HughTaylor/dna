import csv
import sys

dna_seq = ''


def main():
    CSV_file, DNA_sequence_file = get_args()
    sequences, individuals = open_csv_file(CSV_file)
    open_dna_seq(DNA_sequence_file)

    # For each of the STRs (from the first line of the CSV file),
    # This iterates over the search sequences in the column headings of the CSV file
    # And sends them to the computer_max_str_run_len function
    # The results of which are assigned to a list called str_run_lengths
    str_run_lengths = []
    for i in range(len(sequences) - 1):
        str_run_lengths.append(compute_max_str_run_len(sequences[i + 1]))

    matched_individual = compute_matching_individual(str_run_lengths, individuals)
    if matched_individual:
        print(f'{matched_individual}')
    else:
        print('No match')


def get_args():
    if len(sys.argv) == 3:
        return sys.argv[1], sys.argv[2]
    else:
        print(f"Incorrect number of args, expected 2 got {len(sys.argv) - 1}")
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit()
    # returns name of CSV file containing STR counts for a list of individuals
    # returns the name of a text file containing the DNA sequence to identify.
    # if incorrect number of command-line arguments, print an error message
    # assumes first argument is filename of
    # a valid CSV file, and second argument is the filename of a valid text file.


def open_csv_file(filename):
    # print(f"opening CSV file {filename}")
    try:
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            individuals = []
            for row in csv_reader:
                if line_count == 0:
                    sequences = row  # saves the list of
                    line_count += 1
                else:
                    individuals.append(row)  # Hopefully this adds list of sequences to list of users
                    line_count += 1
            # print(f"Processed {line_count} lines.")
    except IOError as e:
        print(f"I/O Error({e.errno}): {e.strerror}")
        sys.exit()
    except:  # handle other exceptions such as attribute errors
        print("Unexpected error")  # print "Unexpected error:", sys.exc_info()[0]
        sys.exit()
    return sequences, individuals

    # open the CSV file and read its contents into memory.
    # You may assume that the first row of the CSV file will be the column names. The first column will be the word name and the
    # remaining columns will be the STR sequences themselves.


def open_dna_seq(filename):
    global dna_seq
    #print(f"opening dna file {filename}")
    # Load DNA sequence into memory
    try:
        with open(filename, 'r') as f:
            dna_seq = f.read()  # Hopefully this will load the whole file into a string called dna_seq
        if not dna_seq:
            print(f"no data in file {filename}")
            sys.exit()
    except IOError as e:
        print(f"I/O Error({e.errno}): {e.strerror}")
        sys.exit()
    except:  # handle other exceptions such as attribute errors
        print("Unexpected error")  # print "Unexpected error:", sys.exc_info()[0]
        sys.exit()
    #print(f"Processed {len(dna_seq)} nucleotides.")


def compute_max_str_run_len(STR):
    # compute the longest run of consecutive repeats of the STR in the DNA sequence to identify.
    maxcount = 0
    end = 0
    start = 0
    while True:  # iterates over the
        count = 0
        start = dna_seq.find(STR, start)  # finds any matches after the last found match (starting at 0)
        if start < 0:  # if there aren't any matches break
            break
        end = start + len(STR)
        while dna_seq.find(STR, start, end) > -1:
            start = end
            end = end + len(STR)
            count += 1
        if count > maxcount:
            maxcount = count
    #print(f"Sequence analysed: {STR}, matches: {maxcount}")
    return(maxcount)


def compute_matching_individual(run_lens, individuals):
    found_individual = ''
    for sublist in individuals:
        for i in range(len(run_lens)):
            if int(sublist[i + 1]) != run_lens[i]:
                break
            elif len(run_lens) == i + 1:
                found_individual = sublist[0]
    return found_individual
    # If the STR counts match exactly with any of the individuals in the CSV file, your program should print out the name of the matching individual.
    #     You may assume that the STR counts will not match more than one individual.
    #     If the STR counts do not match exactly with any of the individuals in the CSV file, your program should print "No match".


main()
