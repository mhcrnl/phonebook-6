import csv
from person import Person

class Phonebook(object):
    def __init__(self, filename, person_dicts):
        self.filename = filename
        self.people = []
        if person_dicts is not []:
            for person in person_dicts: 
                p = Person(person)
                self.people.append(p)

    def create(self, filename):
        """
        Creates a new, empty phonebook file
        """
        # TODO: validate input (here?)
        self.filename = filename
        # prevent overwrites
        file_exists = True
        try:
            f = open(filename)
        except IOError:
            file_exists = False
        if file_exists:
            print ("Not created: file named %s already exists" % filename)
        else:
            # create storage file
            with open(self.filename, 'wb') as output_file:
                fieldnames = ['First Name', 'Last Name', 'Phone Number']
                csvwriter = csv.DictWriter(output_file, fieldnames)
                csvwriter.writerow(dict((fn, fn) for fn in fieldnames))
                return ("created phonebook %s in the current directory" % self.filename)


    def lookup(self, search_name):
        """
        Looks up a person by name in an existing phonebook
        """
        output = ''
        for person in self.people:
            full_name = ' '.join((person.first_name, person.last_name))
            if search_name in full_name:
                # not sure I really like returning 'output' here.
                # I'd like to just print things as they come up,
                # but this is easier to test.
                person_string = ' '.join([person.first_name, person.last_name, str(person.phone_number)])
                if output == '':
                    output = person_string
                else:
                    output = '\n'.join([output, person_string])

        if output == '':
            return "No entries found."
        else:
            return output

    def add(self, name, number):
        names = name.split()
        first_name = names[0]
        if names[1]:
            # last name might be multiple words
            last_name = ' '.join(names[1:])
        else:
            last_name = None
        person_dict = { 'First Name' : first_name,
                        'Last Name' : last_name,
                        'Phone Number' : number
                        }
        p = Person(person_dict)

        # wrap this next stuff in something that makes it atomic
        try:
            self.people.append(p)
            with open(self.filename, "a") as f:
                f.write(p)
        except:
            print "System error: failed to add person to phonebook."

