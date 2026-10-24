function paper2_assert(condition,identifier,message,observed,expected,k,boutKey)
% Comparison values and location are flushed to JSON before raising.
if condition,return;end
context=paper2_error_context('get');
if nargin<6,k=context.source_index;end
if nargin<7,boutKey=context.bout_key;end
method="not_applicable";if isfinite(k),method="F"+k;end
record=struct('status','STOPPED','identifier',identifier,'message',message,'bout_key',string(boutKey),'source_index',k,'k',k,'method_source',method,'observed',observed,'expected',expected,'observed_repr',string(value_text(observed)),'expected_repr',string(value_text(expected)),'stack',{dbstack('-completenames')});
paper2_error_context('failure',record);
error(identifier,'%s | bout=%s k=%g observed=%s expected=%s',message,string(boutKey),k,value_text(observed),value_text(expected));
end
function s=value_text(v)
if isnumeric(v)||islogical(v),s=mat2str(v,17);else,s=jsonencode(v);end
end
