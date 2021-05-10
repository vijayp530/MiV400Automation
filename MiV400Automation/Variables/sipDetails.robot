*** Variables ***

${sip_Response_code}    sip.Status-Code
${Request_Line}     sip.Request-Line
${sipMethod}    sip.Method
${Via}    sip.Via
${Via_Header_Transport}    sip.Via.Transport
${Via_Header_Sent_Address}    sip.Via.sent-by.address
${Via_Header_Sent_Port}    sip.Via.sent-by.port
${Via_Header}    alias
${Via_Header_Branch}    sip.Via.branch
${Via_Header_Rport}    sip.Via.rport
${Route}    sip.Route
${Route_Header_URI}    sip.Route.uri
${Route_Header_Host}    sip.Route.host
${Route_Header_Parameters}    sip.Route.param
${Max_Fowards}    sip.Max-Forwards
${From}    sip.From
${From_Header_User}    sip.from.user
${From_Header_Host}    sip.from.host
${From_Header_Tag}    sip.from.tag
${To}    sip.To
${To_Header_User}    sip.to.user
${To_Header_Host}    sip.to.host
${To_Header_Parameters}    sip.to.param
${Call_ID}    sip.Call-ID
${CSeq}    sip.CSeq
${CSeq_Header_Seq}    sip.CSeq.seq
${CSeq_Header_Method}    sip.CSeq.method
${Accept_Language}    sip.Accept-Language
${Allow}    sip.Allow
${Allow_Events}    sip.Allow-Events
${Contact_Header}    sip.Contact
${Contact_Header_URI}    sip.contact.uri
${Contact_Header_User}    sip.contact.user
${Contact_Header_Host}    sip.contact.host
${Contact_Header_Port}    sip.contact.port
${Contact_Header_Parameters}    sip.contact.parameter
${Supported}    sip.Supported
${User_Agent}    sip.User-Agent
${Content_Type}    sip.Content-Type
${Content_Length}    sip.Content-Length
${Record-Route}    sip.Record-Route
${Expires}    sip.Expires
${Min-Expires}    sip.Min-Expires
${Retry-After}    sip.Retry-After
${Request-Disposition}    sip.Request-Disposition
${Accept-Contact}    sip.Accept-Contact
${Reject-Contact}    sip.Reject-Contact
${Event}    sip.Event
${Subscription-State}    sip.Subscription-State
${Call-Info}    sip.Call-Info
${Error-Info}    sip.Error-Info
${Alert-Info}    sip.Alert-Info
${Reply-To}    sip.Reply-To
${In-Reply-To}    sip.In-Reply-To
${Organization}    sip.Organization
${Priority}    sip.Priority
${Server}    sip.Server
${Subject}    sip.Subject
${Timestamp}    sip.Timestamp
${SIP-ETag}    sip.SIP-ETag
${SIP-If-Match}    sip.SIP-If-Match
${Suppress-Body-If-Match}    sip.Suppress-Body-If-Match
${Suppress-Notify-If-Match}    sip.Suppress-Notify-If-Match
${Remote-Party-ID}    sip.Remote-Party-ID
${P-Asserted-Identity}    sip.P-Asserted-Identity
${P-Preferred-Identity}    sip.P-Preferred-Identity
${Proxy-Require}    sip.Proxy-Require
${Require}    sip.Require
${Unsupported}    sip.Unsupported
${Path}    sip.Path
${Service-Route}    sip.Service-Route
${Accept-Encoding}    sip.Accept-Encoding
${Content-Disposition}    sip.Content-Disposition
${Content-Encoding}    sip.Content-Encoding
${Content-Language}    sip.Content-Language
${MIME-Version}    sip.MIME-Version
${Warning}    sip.Warning
${RAck}    sip.RAck
${RSeq}    sip.RSeq
${Reason}    sip.Reason
${Refer-To}    sip.Refer-To
${Referred-By}    sip.Referred-By
${Replaces}    sip.Replaces
${Refer-Sub}    sip.Refer-Sub
${Authorization}    sip.Authorization
${Proxy-Authenticate}    sip.Proxy-Authenticate
${Proxy-Authorization}    sip.Proxy-Authorization
${WWW-Authenticate}    sip.WWW-Authenticate
${Authentication-Info}    sip.Authentication-Info
${Proxy-Authentication-Info}    sip.Proxy-Authentication-Info
${Security-Client}    sip.Security-Client
${Security-Server}    sip.Security-Server
${Security-Verify}    sip.Security-Verify
${Privacy}    sip.Privacy
${Session-Expires}    sip.Session-Expires
${Min-SE}    sip.Min-SE

#----SDP Parameters--------------
${SDP_Parametrs}    sdp.media_attr
${startWireshark}    start
${stopWireshark}     stop