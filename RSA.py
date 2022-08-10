import random
class RSA:
    def __init__(self,messege): # The constructor accepts only the messege to be encrypted and decrypted 
        self.messege=messege
  
    def prime_generator(self,number):
        '''
        This function will generate prime numbers for us up to the Keylimit given by the user 
        '''  
        if number>2000:           # This a way to make the range smaller for the prime generation to be faster 
            start=number-2000
        else:
            start=2    
        primes=[]
        for num in range(start, number):     # num starts from 2 to the given number
            for x in range(2, num):   # check if x can be divided by num 
                if num % x == 0:      # if true then num is not prime
                    break
            else:                   
                primes.append(num)  # Accumulate all the primes that are there from 2 to the given number in the primes list.
        return primes                   

    def isPrime(self,number):
        """
         This function will determine if the given number is prime or not with a return value of boolean.
        """

        # 0, 1, -ve numbers not prime
        if number < 2:
            return False

        primes =self.prime_generator(number) 
        if number not in primes:
            return False

        return True


    def isCoPrime(self,num1, num2):
        """
         This function will determine if P and q are relatively prime or co prime .
            relatively prime
        """

        return self.gcd(num1, num2) == 1  # will return a boolean value

    def gcd(self,num1, num2):
        """
          This is the euclidean algorithm to find gcd of p and q.  We used the iterative way of this algorithm
        """
        while num2:
            num1, num2 = num2, num1 % num2
        return num1  


    # default keylimit 1000 the keylimit is the max range of prime numbers that p and q can be chosen from at random          
    def generate_keys(self,keylimit=1000):
        '''
         This  function will help us generate public keys and private keys for the encryption and decription to work
         The public key consists of the modulus n and the public (or encryption) exponent e so the public key would be (e,N)
         The private key consists of the private (or decryption) exponent d, which must be kept secret. The private key would be (d,N)

        '''
        e = d = N = 0
        #Choose prime numbers p and q and they should not be equal 
        #The user can enter prime numbers of his/her choice or can specify a keylimmit or choose to go with the random generator of default keylimit of 1000
        askForNumbers = input("Do you want to give prime number your self for the encryption?[Y/N]").upper()
        if askForNumbers == "Y":
            p = int(input("Enter a prime number: ")) # you can give more that 10 digit prime numbers too 
            q = int(input("Enter another prime number: "))
            if p==q:
                raise ValueError("p and q cannot be equal")
        else:
            #For the range up to 40,000 it will work with in considerable time
            askForKeylimit = input("Do you want to give a max range limit for the program to choose primes from?[Y/N]").upper()  
            if askForKeylimit=="Y":
                keylimit=int(input("Enter a range: "))
            primes=self.prime_generator(keylimit)
            while True:
                temp = random.choice(primes)
                if temp>=7:      # Its greater than or equal to 7 because for 2,3 and 5 it won't work eventhough they are primes 
                    p=temp
                    break
            while True:
                temp = random.choice(primes)
                if temp!=p and temp>=7:  # We're making sure that p and q will never be equal otherwise a value error will happen
                    q = temp
                    break             
        N = p * q # compute the RSA Modulus
        totient = (p - 1) * (q - 1) # totient

        # Choose an integer e such that 1 < e < totient 
        # e is coprime with totient; that is, gcd(e, totient) = 1
        while True:
            e = random.randrange(2, totient)
            if (self.isCoPrime(e, totient)):
                break

        # Choose d 
        # d is the modular multiplicative inverse of e modulo totient; that is, d ≡ e−1 (mod totient)
        d = self.modularInverse(e, totient)
        publicKeys=(e,N)
        privateKeys=(d,N)
        print(f"PublicKeys: {publicKeys}")
        print(f"PrivateKeys:{privateKeys} Keep them private as the name suggests")
        return publicKeys,privateKeys  


    def extended_gcd(self,a, b):
        """This funtion will yeild gcd(a,b), x, y s such that a*x + b*y = gcd(a, b)."""
        if a == 0:
            return (b, 0, 1)
        else:
            gcd, y, x = self.extended_gcd(b % a, a)
            return (gcd, x - (b // a) * y, y)  

    def modularInverse(self,a, b):
        '''
        This function is for calculating modulo multiplicative inverse of integer e given by
		the equation 
			d*e mod(totient) = 1   where d is the modular inverse of e and the totient
        '''
        gcd, x, y = self.extended_gcd(a, b)
        if x < 0:
            x += b
        return x   


    def encrypt(self,publicKeys):
        '''
        This function  will return the encrypted messege using the public keys
        '''
        e,N=publicKeys
        cipher = ""
        for letter in self.messege:
            asc_val = ord(letter) # taking the ASCII value of the letter 
            cipher += str(pow(asc_val, e, N)) + " "  # Return the value of asc_val to the power of e (exponent), modulus N (RSA modulo)  and casting it to a string and adding it to the cipher messege
        self.messege=cipher
        return self.messege


    def decrypt(self,privateKeys):
        '''
        This function will return the original messege from the encrypted  messege using the private keys
        '''
        d,N=privateKeys
        messege = ""
        nums = self.messege.split() # using the split funtion to split the string by space in to a list 
        for num in nums:
            if num:
                l = int(num)
                messege += chr(pow(l, d, N)) # returing to the character from the ASCII value to get the ASCII value take l to the power of d (modular inverse), modulus N (RSA modulo)  and casting it to a string and adding it to the cipher messege
        self.messege=messege
        return self.messege


def main():
    messege=input("Enter a messege: ")
    newCipher=RSA(messege) 
    publicKeys,privateKeys=newCipher.generate_keys()
    # enc=newCipher.encrypt(publicKeys)
    dec=newCipher.decrypt(privateKeys) 
    print(f"Messege:{messege}") 
    # print(f"Encryption:{enc}")
    print(f"Decryption:{dec}")
main()              

