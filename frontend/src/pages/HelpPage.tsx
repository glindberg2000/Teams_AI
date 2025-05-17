export default function HelpPage() {
    return (
        <div className="flex flex-col items-center justify-center h-full py-16 bg-gradient-to-br from-[#4FC3F7]/20 to-[#1565C0]/10 w-full">
            <h2 className="text-3xl font-bold mb-4 text-[#1565C0]">Help & Support</h2>
            <p className="text-lg text-blue-900 max-w-xl text-center mb-4">
                Need help with TEAM AI? Check the documentation or contact support for assistance with teams, roles, secrets, or chat workflows.
            </p>
            <div className="text-blue-800">Email: <a href="mailto:support@teamai.example" className="underline">support@teamai.example</a></div>
        </div>
    );
} 