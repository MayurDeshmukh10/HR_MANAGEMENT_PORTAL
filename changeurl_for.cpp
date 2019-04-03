/*
Code to change the normal html file to flask back end
*/

#include<iostream>
#include<fstream>
#include<cstring>
using namespace std;
bool checkSubstring(string cStr, string cSub)		//check substring
{
	int nI=0,nJ=0;
	bool bFlag=0;
	for(nI=0;cStr[nI]!='\0';nI++)
	{
		if(cStr[nI]==cSub[nJ])
		{
	
			nJ++;
			bFlag=1;
			if(cSub[nJ]=='\0')
			{
				bFlag=1;
				break;
			}
			else if(cStr[nI+1]!=cSub[nJ])
			{
				nJ=0;
			}
		}
		else if(cStr[nI]!=cSub[nJ])
		{
			bFlag=0;
		}
	} //end of "i" for
	return bFlag;		//returns 1 if substring is present
} //end of function substring

int main(int argc, char **argv)
{
    fstream file;
    //cout<<"ARGC: "<<argc<<endl;
    //cout<<argv[1]<<endl;
    ifstream inFile(argv[1]);
    ofstream outFile(argv[2]);
    string line;
    string newline;
    bool flag = false;
    string checkcss = "<link href=\"assets/";
    string checkjs = "<script src=";
   int linecount = 1;

   string doublequotes = "\"";

    while(getline(inFile,line))
    {
        newline = "";
        cout<<"[ "<<linecount<<" ] ";
        cout<<line<<"\n";
        string link;
        int fp_start_index = 0;     //file position start index
        int fp_end_index = 0;       //file position end index
        int count=0;
        if(checkSubstring(line,checkcss))
        {
            //get actual start and end points of file position
            cout<<"[---css found---]";
            for(int i=0;i<line.length();i++)
            {
                if(line[i] == doublequotes[0])
                {
                    if(count == 0)
                    {
                        fp_start_index = i;
                        count++;
                    }
                    else if(count == 1)
                    {
                        fp_end_index = i;
                        count++;
                    }
                    else if(count > 1)
                        break;
                }
            }
            //cout<<line<<endl;
            string path_to_file = line.substr(fp_start_index+1,(fp_end_index-fp_start_index-1));
            cout<<"\npath to file: "<<path_to_file<<endl;
            string end_ofline = line.substr(fp_end_index+1);
            cout<<"end of line: "<<end_ofline<<endl;

            newline.append(line,0,fp_start_index);
            newline.append("\"{{url_for('static',filename='");
            newline.append(path_to_file);
            newline.append("')}} \"");
            newline.append(end_ofline);
            cout<<"\nEdited Line: "<<newline<<endl;

        }
        else if(checkSubstring(line,checkjs))
        {
            //get actual start and end points of file position
            cout<<"[---js found---]";
            for(int i=0;i<line.length();i++)
            {
                if(line[i] == doublequotes[0])
                {
                    if(count == 0)
                    {
                        fp_start_index = i;
                        count++;
                    }
                    else if(count == 1)
                    {
                        fp_end_index = i;
                        count++;
                    }
                    else if(count > 1)
                        break;
                }
            }
            //cout<<line<<endl;
            string path_to_file = line.substr(fp_start_index+1,(fp_end_index-fp_start_index-1));
            cout<<"\npath to file: "<<path_to_file<<endl;
            string end_ofline = line.substr(fp_end_index+1);
            cout<<"end of line: "<<end_ofline<<endl;

            newline.append(line,0,fp_start_index);
            newline.append("\"{{url_for('static',filename='");
            newline.append(path_to_file);
            newline.append("')}} \"");
            newline.append(end_ofline);
            cout<<"\nEdited Line: "<<newline<<"\n\n";
        }
        else
        {
            newline = line;
        }
        newline.append("\n");
        outFile << newline;
        linecount++;
    }

    return 0;
}